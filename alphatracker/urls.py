from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alphatracker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^content/', include('content.urls')),
    url(r'^userprofile/', include('userprofile.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
