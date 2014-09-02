from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
        url(r'^$', views.recent, name='recent'),
        url(r'(?P<page>\d+)/', views.recent, name='recent_page'),
        url(r'post/(?P<slug>[-\w]+)/$', views.post, name='post'),
        url(r'submit/$', views.submit, name='submit')
)