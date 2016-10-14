from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Media

class Home(ListView):
	template_name="home.html"
	model = Media
	paginate_by = 12

home = Home.as_view()


class DetailMedia(DetailView):
    model = Media
    
detail = DetailMedia.as_view()
