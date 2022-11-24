from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeaturesListView.as_view() , name="list_features_url"),
    path('detail/<int:pk>', views.FeaturesDetailView.as_view() , name="detail_features_url"),

]

