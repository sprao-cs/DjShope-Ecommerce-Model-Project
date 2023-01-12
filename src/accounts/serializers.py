from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    cpassword = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'cpassword']
        extra_kwargs = {
            'password': {'write_only':True},
            'cpassword': {'write_only':True}
        }
    

    def create(self, validated_data):
        firstName = validated_data.get('first_name')
        lastName = validated_data.get('last_name')
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        cpassword = validated_data.get('cpassword')

        if password == cpassword:
            user = User(username=username, email=email, first_name=firstName, last_name=lastName)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': "Password Does not match"
            })