from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer


class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
                'user': serializer.data
            })
        return Response(serializer.errors)
        
class LogoutAPIView(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response("success")
        except Exception as e:
            return Response("failed")