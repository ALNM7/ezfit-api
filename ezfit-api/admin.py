from django.contrib import admin
from crud_escolar_api.models import *


@admin.register(FoodAnalysis)
class FoodAnalysisAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'user', 'timestamp')

