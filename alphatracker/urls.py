from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(pattern_name='recent')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^u/', include('userprofile.urls')),
    url(r'^c/', include('content.urls')),
    url(r'^r/', include('ranking.urls'))
)