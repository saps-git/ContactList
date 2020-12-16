from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt

# Create your views here.
 
class RegisterView(GenericAPIView): # GenericAPIView gives the ability to handle all the request types the way you want them to
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(): # will check in the validate method in the serializer file
            serializer.save()  # will run the create method in the serializer file
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        username = data.get('username','')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password) # once the username and password matches a record in DB, it will return the record
        
        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY) #encoding the token
            serializer = UserSerializer(user) #converting into JSON

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK) #returning the data

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    