from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from rest_framework import status,generics
from colorama import Fore,Style
from rest_framework.authtoken.models import Token
#Esto para cambiar la contraseña
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
# Importar el serializador
from .serializers import UserSerializer,ChangePasswordSerializer
import json
from django.urls import reverse

# Create your views here.

def index(request):
    print(Fore.GREEN + "Successfully")
    print(Style.RESET_ALL)
    context = {
        'reset_password_url': "{}?token={}"
    }
    return render(request,'index.html',context)

class LoginView(APIView):
    def post(self, request):
        #Recuperamos las credenciales y autenticamos al usuario
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        user = authenticate(email=email,password=password)

        #Si es correcto añadimos a la request la informacion de sesion
        if user:
            login(request,user)
            return Response(status=status.HTTP_200_OK)
        # Si no es correcto devolvemos un error en la pertición
        return Response(status=status.HTTP_404_NOT_FOUND)

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    return Response({"user":request.user.email},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



