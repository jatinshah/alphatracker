from django.conf.urls import patterns, url
from userprofile import views as userprofile_views
from django.contrib.auth.views import login, logout
from alphatracker.settings import LOGIN_REDIRECT_URL

urlpatterns = patterns('',
                       url(r'^edit/$', userprofile_views.edit_profile, name='edit'),
                       url(r'^(?P<username>[-\w\.+@]+)/$', userprofile_views.profile, name='profile'),
)