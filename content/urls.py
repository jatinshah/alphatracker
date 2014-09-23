from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
        url(r'^post/(?P<slug>[-\w]+)/$', views.post, name='post'),
        url(r'^recent/(?P<page>\d+)/$', views.get_feed, name='recent_page'),
        url(r'^recent/$', views.get_feed, name='recent'),
        url(r'^follow/(?P<page>\d+)/$', views.get_following, name='follow_page'),
        url(r'^follow/$', views.get_following, name='follow'),
        url(r'^submit/$', views.submit, name='submit'),
        url(r'^add_comment/$', views.add_comment, name='add_comment'),
        url(r'^vote/$', views.vote_post, name='vote'),
        url(r'^vote_comment/$', views.vote_comment, name='vote_comment')
)