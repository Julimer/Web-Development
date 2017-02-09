import django.contrib.auth.views
from django.conf.urls import url
from django.contrib import admin
from grumblr import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^followStream$', views.followStream, name='followStream'),
    url(r'^userlogin$', views.userlogin, name='userlogin'),
    url(r'^userlogout$', views.userlogout, name='userlogout'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^register$', views.register, name='register'),

    url(r'^post$', views.post, name='post'),

    url(r'^editProfile$', views.editProfile, name='editProfile'),
    url(r'^confirm/(?P<id>\d+)/(?P<token>.+)$', views.confirm, name='confirm'),
    url(r'^follow/(?P<id>\d+)$', views.follow, name='follow'),

    url(r'^globalStream/?$', views.updatePosts, name='updatePosts'),
    url(r'^globalStream/(?P<time>.+)$', views.updatePosts, name='updatePosts'),

    url(r'^addComment/', views.addComment, name='addComment'),
    url(r'^profile/addComment/', views.addComment, name='profile_addComment'),

    url(r'^changepassword$', django.contrib.auth.views.password_change,
        {'template_name': 'password_change.html'}, name='password_change'),
    url(r'^changepassword/done/$', django.contrib.auth.views.password_change_done,
        {'template_name': 'password_change_done.html'}, name='password_change_done'),

    url(r'^resetpassword/$', django.contrib.auth.views.password_reset,
        {'post_reset_redirect': 'password_reset_done', 'template_name': 'password_reset.html'}, name="password_reset"),
    url(r'^resetpassword/passwordsent/$', django.contrib.auth.views.password_reset_done,
        {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', django.contrib.auth.views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'}, name='password_reset_complete') ,

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
