from django.conf.urls import patterns, url
from ranking import views

urlpatterns = patterns(
    '',
    url(r'stocks/$', views.get_stock_symbols, name='stocks')
)