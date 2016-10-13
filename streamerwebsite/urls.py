from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from base.views import home 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home , name="home")
] + staticfiles_urlpatterns()
