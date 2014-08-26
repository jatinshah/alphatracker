from django.conf.urls import patterns, url
from userprofile import views

urlpatterns = patterns('',
        url(r'^$', views.profile, name='profile'),
        url(r'login/$', views.user_login, name='login'),
        url(r'logout/$', views.user_logout, name='logout'),
        url(r'signup/$', views.signup, name='signup'),
)