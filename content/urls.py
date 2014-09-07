from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
        url(r'^post/(?P<slug>[-\w]+)/$', views.post, name='post'),
        url(r'^recent/(?P<page>\d+)/$', views.get_feed, name='recent_page'),
        url(r'^recent/$', views.get_feed, name='recent'),
        url(r'^(?P<page>\d+)/$', views.get_feed, {'order': 'trending'}, name='trending_page'),
        url(r'^$', views.get_feed, {'order': 'trending'}, name='trending'),
        url(r'^submit/$', views.submit, name='submit'),
        url(r'^add_comment/$', views.add_comment, name='add_comment'),
)