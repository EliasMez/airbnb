from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

class FeaturesListView(ListView):
    model = Feature
    template_name = "features/features_list.html"
    context_object_name = 'features_list'

class FeaturesDetailView(DetailView):
    model = Feature
    template_name = "features/features_detail.html"

