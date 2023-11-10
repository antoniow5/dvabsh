from django.contrib.auth.models import User
from rest_framework import serializers

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'email': {'required': True, "allow_blank": False}, 'password': {'required': True}} 