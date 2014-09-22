from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
        url(r'^post/(?P<slug>[-\w]+)/$', views.post, name='post'),
        url(r'^recent/(?P<page>\d+)/$', views.get_feed, name='recent_page'),
        url(r'^recent/$', views.get_feed, name='recent'),
        url(r'^myfeed/(?P<page>\d+)/$', views.get_myfeed, name='myfeed_page'),
        url(r'^myfeed/$', views.get_myfeed, name='myfeed'),
        url(r'^submit/$', views.submit, name='submit'),
        url(r'^add_comment/$', views.add_comment, name='add_comment'),
        url(r'^vote/$', views.vote_post, name='vote'),
        url(r'^vote_comment/$', views.vote_comment, name='vote_comment')
)