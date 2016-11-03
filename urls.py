__author__ = 'tbartel'
from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^(?P<my_instance_name>[\w-]+)/$', instance_detail, name='instance-detail'),
    url(r'^(?P<my_instance_name>[\w-]+)/graph/$', instance_graph),
    url(r'^(?P<my_instance_name>[\w]+)/(?P<my_payment_method_name>[a-z-,]+)/graph/$', instance_graph),
    url(r'^$', instance_overview, name='instance-detail'),
]