from django.conf.urls import patterns, url
from content import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'link/$', views.link, name='link'),
        url(r'text/$', views.text, name='text'),
        url(r'submit/$', views.submit, name='submit')
)