from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Media, Resource, MainMedia

class Home(ListView):
    template_name="home.html"
    model = Media
    paginate_by = 20

    def get_queryset(self):
        qs = super(Home, self).get_queryset()
        filter = self.kwargs.get("filter")
        if filter:
            if "ser" in filter:
                qs = qs.filter(type="ser")
            elif "mov" in filter:
                qs = qs.filter(type="mov")
        return qs
    def get_context_data(self, **context):
        context = super(Home,self).get_context_data(**context)
        context.update({
                'main_media':MainMedia.objects.all(),
                'active':self.kwargs.get("filter","series")
            })
        return context

home = Home.as_view()

filter_home = Home.as_view()

class DetailMedia(DetailView):
    model = Media

detail = DetailMedia.as_view()

class DetailResource(DetailView):
    model = Resource



view = DetailResource.as_view()
