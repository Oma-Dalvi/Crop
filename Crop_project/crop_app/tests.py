from django.test import TestCase
from rest_framework.test import APITestCase
# from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
from django.contrib.auth.hashers import make_password

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import pandas as pd
import requests


class UserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        url = reverse('register_user')
        _data = {
            "username": "Dhoni",
            "password": "123"
        }
        _response = self.client.post(url, data=_data, format="json")
        self.assertEqual(_response.status_code, status.HTTP_200_OK)

    def test_login(self):
        hashed_password = make_password('123')
        obj = User.objects.create(username="Dhoni", password=hashed_password)

        url = reverse('login_user')
        _data = {
            "username": "Dhoni",
            "password": '123'
        }
        _response = self.client.post(url, data=_data, format="json")
        self.assertEqual(_response.status_code, status.HTTP_200_OK)


import unittest
from unittest.mock import patch, Mock


def call_third_party_api():
    openmeteo = openmeteo_requests.Client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        # "current": ["temperature_2m", "precipitation", "cloud_cover"],
        "hourly": ["temperature_2m", "precipitation", "cloud_cover"],
        "past_days": 2
    }
    responses = openmeteo.weather_api(url, params=params)
    response = requests.get(url, params=params)
    return response.json()


class SecondTest(unittest.TestCase):
    @patch('call_third_party_api.openmeteo.weather_api')
    def test_your_function(self, mock_weather_api):
        # Mock the response from openmeteo.weather_api
        mock_response = {
            "hourly": {
                "temperature_2m": [20.0, 21.0, 22.0],
                "precipitation": [0.0, 0.5, 1.0],
                "cloud_cover": [10, 20, 30],
                "time": [datetime.now().timestamp(), (datetime.now() + timedelta(hours=1)).timestamp(),
                         (datetime.now() + timedelta(hours=2)).timestamp()],
                "time_end": [(datetime.now() + timedelta(hours=1)).timestamp(),
                             (datetime.now() + timedelta(hours=2)).timestamp(),
                             (datetime.now() + timedelta(hours=3)).timestamp()],
                "interval": 3600
            }
        }

        # Configure the mock to return the desired response
        mock_weather_api.return_value = [mock_response]

        # Call the function that uses openmeteo.weather_api
        result = call_third_party_api()

        expected_result = {
            "date": pd.date_range(
                start=pd.to_datetime(mock_response["hourly"]["time"][0], unit="s"),
                end=pd.to_datetime(mock_response["hourly"]["time_end"][-1], unit="s"),
                freq=pd.Timedelta(seconds=mock_response["hourly"]["interval"]),
                inclusive="left"
            ),
            "temperature_2m": mock_response["hourly"]["temperature_2m"],
            "precipitation": mock_response["hourly"]["precipitation"],
            "cloud_cover": mock_response["hourly"]["cloud_cover"]
        }

        # Assert that the function returns the expected result
        self.assertEqual(result, expected_result)
