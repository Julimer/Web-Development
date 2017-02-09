import django.contrib.auth.views
from django.conf.urls import include, url
from django.contrib import admin
from grumblr import views
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
   url(r'^admin/', admin.site.urls),
   url(r'^', include('grumblr.urls')),
   url(r'^$', views.globalStream, name='globalStream'),
]
