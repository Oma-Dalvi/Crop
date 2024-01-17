from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class HourlyDataSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    temperature_2m = serializers.FloatField()
    precipitation = serializers.FloatField()
    cloud_cover = serializers.FloatField()

    def to_representation(self, instance):
        # Convert the DataFrame row to a dictionary
        return {
            'date': instance['date'],
            'temperature_2m': instance['temperature_2m'],
            'precipitation': instance['precipitation'],
            'cloud_cover': instance['cloud_cover'],
        }