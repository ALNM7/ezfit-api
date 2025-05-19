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
from rest_framework.permissions import AllowAny


import requests


class FoodAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        foods = FoodAnalysis.objects.filter(user=request.user).order_by("-timestamp")
        data = FoodAnalysisSerializer(foods, many=True).data
        
        return Response(data, 200)
    
class FoodView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Obtener un registro por ID
    def get(self, request, *args, **kwargs):
        food_id = request.GET.get("id")
        food = get_object_or_404(FoodAnalysis, id=food_id, user=request.user)
        data = FoodAnalysisSerializer(food, many=False).data
        return Response(data, status=status.HTTP_200_OK)

    # Crear un nuevo análisis de imagen
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({"error": "No se envió ninguna imagen."}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        food_record = FoodAnalysis.objects.create(user=request.user, image=image_file)
        image_path = food_record.image.path

        try:
            # API LogMeal
            api_user_token = '507d2096146097898b1235a9b63cefcb4af1d6fe'
            headers = {'Authorization': f'Bearer {api_user_token}'}

            # Segmentación
            segmentation_url = 'https://api.logmeal.com/v2/image/segmentation/complete'
            with open(image_path, 'rb') as img:
                resp_seg = requests.post(segmentation_url, files={'image': img}, headers=headers)
            resp_seg.raise_for_status()
            image_id = resp_seg.json().get('imageId')
            if not image_id:
                raise Exception("No se obtuvo imageId de la API.")

            # Nutrición
            nutritional_url = 'https://api.logmeal.com/v2/recipe/nutritionalInfo'
            resp_nutr = requests.post(nutritional_url, json={'imageId': image_id}, headers=headers)
            resp_nutr.raise_for_status()
            nutritional_data = resp_nutr.json()

            # Datos clave
            nutri_info = nutritional_data.get('nutritional_info', {})
            total_nutrients = nutri_info.get('totalNutrients', {})
            calories = nutri_info.get('calories')
            fat = total_nutrients.get('FAT', {}).get('quantity')
            carbs = total_nutrients.get('CHOCDF', {}).get('quantity')
            protein = total_nutrients.get('PROCNT', {}).get('quantity')
            sodium = total_nutrients.get('NA', {}).get('quantity')
            food_name = nutritional_data.get('foodName', ['Desconocido'])[0]

            # Guardar análisis completo
            food_record.food_name = food_name
            food_record.calories = calories or 0
            food_record.analysis_data = nutritional_data
            food_record.save()

            filtered_data = {
                "food_name": food_name,
                "calories": calories,
                "fat": fat,
                "carbs": carbs,
                "protein": protein,
                "sodium": sodium,
            }

            return Response({
                "message": "Análisis realizado con éxito.",
                "data": filtered_data,
                "id": food_record.id  # ✅ para redirigir a detalle en el frontend
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
