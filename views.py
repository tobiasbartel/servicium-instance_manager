from django.shortcuts import render
from models import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import datetime
from pprint import pprint
import pydotplus
import re
from main.settings import TEMPLATE_NAME
from instance_manager import graphgenerator
from machine_manager.models import Machine
from contact_manager.views import contact_box


def instance_overview(request):
    pass

def instance_graph(request, my_instance_name, my_payment_method_name=None):
    if my_payment_method_name is not None:
        my_graph = graphgenerator.instance(my_instance_name, my_payment_method_name.split(","))
    else:
        my_graph = graphgenerator.instance(my_instance_name)

    response = HttpResponse(my_graph, content_type='image/svg+xml')
    response['Content-Length'] = len(my_graph)
    return response

def instance_detail(request, my_instance_name):
    my_instance = Instance.objects.get(slug=my_instance_name)
    my_contacts = InstanceContact.objects.all().filter(parent=my_instance)
    my_contact_boxes = contact_box(request, my_contacts)

    my_payment_methods = set([])
    for connection in InstanceConnectsInstance.objects.all().filter(from_instance=my_instance):
        for pm in connection.payment_methods.iterator():
            my_payment_methods.add(pm)
    for connection in InstanceConnectsModule.objects.all().filter(from_instance=my_instance):
        for pm in connection.payment_methods.iterator():
            my_payment_methods.add(pm)

    my_payment_methods = sorted(my_payment_methods, key=lambda k: k.name)

    my_machines = Machine.objects.all().filter(instance=my_instance).order_by('zone_id', 'type')

    return render_to_response('%s/instance_detail.tpl.html' % TEMPLATE_NAME, {'request': request, 'my_contact_boxes':my_contact_boxes, 'my_instance': my_instance, 'my_payment_methods': my_payment_methods, 'my_machines': my_machines})

