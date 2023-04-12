from django.contrib import admin
from django.urls import path
from . import views


app_name= "find_villager_home_app"


urlpatterns = [
    path("",views.home_view, name="home"),
    path("thankyou/",views.villager_response, name="response_quiz")
]