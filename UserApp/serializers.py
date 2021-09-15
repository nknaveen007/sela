from django.db import models
from django.db.models import fields
from rest_framework import serializers
from UserApp.models import UserData, Otp


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('UserId', 'UserStatus', 'PhoneNumber', 'Name', 'SelaId')


class OtpSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('number', 'otp')
