from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name')


class PatientDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PatientData
        fields = ('input_place', 'image')


class PatientDataWriteSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PatientData
        fields = '__all__'

class HospitalDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = HospitalData
        fields = '__all__'

