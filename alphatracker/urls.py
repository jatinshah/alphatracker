from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView

from alphatracker.sitemap import sitemaps

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(pattern_name='recent')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^u/', include('userprofile.urls')),
    url(r'^c/', include('content.urls')),
    url(r'^r/', include('ranking.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^terms/$', 'flatpage', {'url': '/terms/'}, name='terms'),
    url(r'^policy/$', 'flatpage', {'url': '/policy/'}, name='policy'),
)