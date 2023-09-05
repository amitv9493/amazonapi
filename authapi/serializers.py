from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid username or password")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")

        else:
            raise serializers.ValidationError("Both username and password are required")

        data['user'] = user
        return data
