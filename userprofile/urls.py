from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
                       url(r'^edit/$', views.edit_profile, name='edit'),
                       url(r'^follow/$', views.follow, name='follow'),
                       url(r'^(?P<username>[-\w\.+@]+)/$', views.profile, name='profile'), #Must be last
)