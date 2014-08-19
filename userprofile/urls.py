from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
        url(r'^$', views.profile, name='profile'),
)