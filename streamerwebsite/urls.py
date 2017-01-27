from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from base.views import detail, home, view, filter_home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home , name="home"),
    url(r'^(?P<filter>series|movies)/$',filter_home , name="filter-home"),
    url(r'^detalle/(?P<slug>[-\w]+)/(?P<pk>[\d]+)/(?P<qua>[\w]+)',view, name="view"),
    url(r'^detalle/(?P<slug>[-\w]+)/$',detail , name="detail"),
   
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

