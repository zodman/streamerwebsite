from django.shortcuts import render
from django.views.generic import ListView
from .models import Media

class Home(ListView):
	template_name="base.html"
	model = Media

home = Home.as_view()