from django.conf.urls import patterns, url
from userprofile import views as userprofile_views
from django.contrib.auth.views import login, logout
from alphatracker.settings import LOGIN_REDIRECT_URL

urlpatterns = patterns('',
        url(r'^$', userprofile_views.profile, name='profile'),
        url(r'login/$', login, {'template_name': 'userprofile/login.html'}, name='login'),
        url(r'logout/$', logout, {'next_page': LOGIN_REDIRECT_URL}, name='logout'),
        url(r'signup/$', userprofile_views.signup, name='signup'),
)