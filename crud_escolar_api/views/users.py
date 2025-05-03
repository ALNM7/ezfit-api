from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from crud_escolar_api.serializers import *
from crud_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json
from django.utils import timezone


class Userme(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        #TODO: Regresar perfil del usuario
        return Response({})

class UsuariosView(generics.CreateAPIView):
    # Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            role = request.data.get('role', 'default')  # Asegurar que role no sea None

            # Validar si el usuario ya existe
            if User.objects.filter(email=email).exists():
                return Response({"message": f"El email {email} ya está en uso."}, status=400)

            # Crear el usuario usando `create_user` para que la contraseña se encripte correctamente
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name, last_login=timezone.now())
            user.first_name = name  # Usar `first_name` en lugar de `name`
            user.is_active = True  # Habilitar el usuario
            user.save()

            # Asignar el usuario a un grupo (si es necesario)
           

            return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
