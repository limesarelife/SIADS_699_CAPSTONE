from django.contrib import admin
from django.urls import path
from . import views


app_name= "find_villager_home_app"


urlpatterns = [
    path("",views.home_view, name="home"),
    path("thankyou/",views.villager_response, name="response_quiz"),
    # path(r'^thanks/$', views.thank_you, name='thank-you'),
]
    # "Option_1":v_name1,"Villager_1":v_img1 ,"Option_2":v_name2, "Villager_2": v_img2}
    # <slug:key>
    # path("<slug:Option_1>/<path:Villager_1>/<slug:Option_2>/<path:Villager_2>", views.final_villager, name="final_vil")
