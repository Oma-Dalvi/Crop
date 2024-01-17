from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .serializers import UserSerializer, UserSigninSerializer,HourlyDataSerializer
from .Authentication import token_expire_handler, expires_in
import pandas as pd

import openmeteo_requests
from openmeteo_sdk.Variable import Variable

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)


class UserRegisterApi(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
        return Response({"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})


class UserSignInApi(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        try:
            signin_serializer = UserSigninSerializer(data=request.data)
            if not signin_serializer.is_valid():
                return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

            user = authenticate(
                username=signin_serializer.data['username'],
                password=signin_serializer.data['password']
            )

            if not user:
                return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

            # Token
            token, _ = Token.objects.get_or_create(user=user)

            is_expired, token = token_expire_handler(token)
            user_serialized = UserSerializer(user)

            return Response({
                'user': user_serialized.data,
                'expires_in': expires_in(token),
                'token': token.key
            }, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'message': 'Something went wrong.'})


class HistoricalDataApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            openmeteo = openmeteo_requests.Client()
            url = "https://api.open-meteo.com/v1/forecast"

            params = request.data
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
            hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )}
            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["precipitation"] = hourly_precipitation
            hourly_data["cloud_cover"] = hourly_cloud_cover

            hourly_dataframe = pd.DataFrame(data=hourly_data)

            serializer = HourlyDataSerializer(hourly_dataframe.to_dict(orient='records'), many=True)
            serialized_data = serializer.data

            return Response({
                'Historic Weather Data':serialized_data
            }, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'message': 'Something went wrong.'})