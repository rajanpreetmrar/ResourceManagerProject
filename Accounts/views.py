import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render

from rest_framework import status, views, permissions
from rest_framework.response import Response
from Accounts.models import UserAccounts
from Accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, PasswordResetSerializer


class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                login(request, user)
                user_details = {'username': user.username, 'email': user.email, 'user_type': user.user_type}
                payload = {
                    'id': user_details,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'message': 'success', 'token': token}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(views.APIView):

    def post(self, request):
        logout(request)
        token = request.COOKIES.get('jwt')
        if token:
            request.COOKIES.pop('jwt', None)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class PasswordResetView(views.APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(UserAccounts, email=serializer.validated_data['email'])
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Home(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = payload.get('id')
        if user['user_type'] == 'superuser' or user['user_type'] == 'Super User':
            pass
            # links = LinkData.objects.all()  # Change the number of links as needed
            # serializer = LinkSerializer(links, many=True)
            # return Response(serializer.data)
        else:
            return render(request, 'home.html')
