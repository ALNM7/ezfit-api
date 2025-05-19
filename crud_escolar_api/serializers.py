from rest_framework import serializers
from rest_framework.authtoken.models import Token
from crud_escolar_api.models import *
from rest_framework import serializers
from .models import FoodAnalysis



class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','name', 'email')



class FoodAnalysisSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False)
    timestamp = serializers.DateTimeField(read_only=True)
    food_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    calories = serializers.FloatField(required=False, allow_null=True)
    analysis_data = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = FoodAnalysis
        fields = (
            'id',
            'user',
            'image',
            'timestamp',
            'food_name',
            'calories',
            'analysis_data'
        )