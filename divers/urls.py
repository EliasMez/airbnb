from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home_url"),
    path('about/', views.about_view, name="about_url"),
    path('about_us/', views.about_us_view, name="about_us_url"),

]

