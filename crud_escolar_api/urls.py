"""point_experts_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crud_escolar_api.views import bootstrap
from crud_escolar_api.views import users
from crud_escolar_api.views import auth
from crud_escolar_api.views import food
from .views.food import FoodAll, FoodView
#Para la subida de fotos
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
       #Version
        path('bootstrap/version', bootstrap.VersionView.as_view()),
    #Create User
        path('user/', users.UsuariosView.as_view()),
    #Login
        path('token/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),
    #Comida 
        # path('food-analysis/', food.FoodAnalysisView.as_view()),
    #Comida ahora si final 
         path('food/all', FoodAll.as_view()),
        path('food', FoodView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


