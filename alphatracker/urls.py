from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from alphatracker.settings import LOGIN_REDIRECT_URL
from userprofile.views import signup

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', login, {'template_name': 'userprofile/login.html'}, name='login'),
                       url(r'^logout/$', logout, {'next_page': LOGIN_REDIRECT_URL}, name='logout'),
                       url(r'^signup/$', signup, name='signup'),
                       url(r'^u/', include('userprofile.urls')),
                       url(r'^c/', include('content.urls')),
                       url(r'^r/', include('ranking.urls')),
)

