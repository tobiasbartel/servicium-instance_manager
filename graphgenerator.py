from models import *
from pprint import pprint
from servicecatalog.models import READ, WRITE, BOTH
import pydotplus
import re

def instance(my_instance_name, my_payment_methods_list=None):

    my_instance=Instance.objects.get(slug=my_instance_name)
    if my_payment_methods_list is not None:
        my_payment_methods = []
        for payment_method in my_payment_methods_list:
            my_payment_methods.append(PaymentMethod.objects.get(slug=payment_method))
    else:
        my_payment_methods = None


    ARROW_SIZE = 0.7
    FONT_SIZE = 8

    graph = pydotplus.Dot(graph_type='digraph', graph_name=my_instance.__unicode__, strict=True)
    # graph.set_prog('fdp')
    graph.set('splines', 'ortho')
    #graph.set('rankdir', 'LR')
    graph.set('overlap', 'false')
    # graph.set('splines',  True)
    graph.set('concentrate', True)
    # graph.set('nodesep', 0.5)
    graph.set('stylesheet', '/static/PaymentFont/css/paymentfont.css')
    # graph.set('newrank', True)
    graph.set('concentrate', True)

    node = pydotplus.Node()
    node.set_name(my_instance.__unicode__())
    node.set('URL', '/instance/%s/' % my_instance.slug)
    node.set('fontsize', FONT_SIZE)
    node.set('fontname', 'PaymentFont,sans-serif')
    node.set('shape', 'box3d    ')
    node.set('style', 'filled')
    node.set('fillcolor', 'gold')
    graph.add_node(node)

    if my_instance.customer_accesable:
        node = pydotplus.Node()
        node.set_name('Merchant')
        node.set('fontsize', FONT_SIZE)
        node.set('fontname', 'PaymentFont,sans-serif')
        node.set('fillcolor', 'cornflowerblue')
        node.set('style', 'filled')
        node.set('shape', 'invhouse')
        graph.add_node(node)
        edge = pydotplus.Edge('Merchant', my_instance.__unicode__())
        edge.set('arrowsize', ARROW_SIZE)
        graph.add_edge(edge)


    for dependency in InstanceConnectsInstance.objects.all().filter(from_instance=my_instance).iterator():
        label = ''
        if my_payment_methods is None or len(dependency.payment_methods.values()) == 0:
            node = pydotplus.Node()
            node.set_name(dependency.to_instance.__unicode__())
            node.set('shape', 'box')
            node.set('URL', '/instance/%s/' % dependency.to_instance.slug)
            node.set('fontsize', FONT_SIZE)
            node.set('fontname', 'PaymentFont,sans-serif')
            graph.add_node(node)

            edge = pydotplus.Edge(dependency.from_instance.__unicode__(), dependency.to_instance.__unicode__())
            edge.set('arrowsize', ARROW_SIZE)
            edge.set('fontsize', FONT_SIZE)
            edge.set('fontname', 'PaymentFont,sans-serif')
            if dependency.comment is not None:
                edge.set('xlabel', dependency.comment)
            if dependency.access_direction == READ:
                edge.set('dir', 'back')
            elif dependency.access_direction == BOTH:
                edge.set('dir', 'both')

            if dependency.is_online:
                edge.set('color', 'red')
            elif dependency.is_online is False:
                edge.set('color', 'blue')

            graph.add_edge(edge)
        else:
            filtered_payment_methods = list(set(dependency.payment_methods.iterator()) & set(my_payment_methods))
            if len(filtered_payment_methods) > 0:
                node = pydotplus.Node()
                node.set_name(dependency.to_instance.__unicode__())
                node.set('shape', 'box')
                node.set('URL', '/instance/%s/' % dependency.to_instance.slug)
                node.set('fontsize', FONT_SIZE)
                node.set('fontname', 'PaymentFont,sans-serif')
                graph.add_node(node)

                edge = pydotplus.Edge(dependency.from_instance.__unicode__(), dependency.to_instance.__unicode__())
                edge.set('fontname', 'PaymentFont,sans-serif')
                edge.set('fontsize', FONT_SIZE)
                edge.set('arrowsize', ARROW_SIZE)

                if dependency.access_direction == READ:
                    edge.set('dir', 'back')
                elif dependency.access_direction == BOTH:
                    edge.set('dir', 'both')

                if dependency.is_online:
                    edge.set('color', 'red')
                elif dependency.is_online is False:
                    edge.set('color', 'blue')

                for depending_paynment_method in filtered_payment_methods:
                    if depending_paynment_method.image is not None:
                        label += "%s" % depending_paynment_method.image
                    else:
                        label += "%s" % depending_paynment_method

                if dependency.comment:
                    label = "%s" % (dependency.comment,)

                edge.set('xlabel', label)
                graph.add_edge(edge)

    for dependency in InstanceConnectsModule.objects.all().filter(from_instance=my_instance):
        label = ''
        if my_payment_methods is None or len(dependency.payment_methods.values()) == 0:
            node = pydotplus.Node()
            node.set_name(dependency.to_module.__unicode__())
            node.set('URL', '/module/%s/' % dependency.to_module.slug)
            node.set('fontsize', FONT_SIZE)
            node.set('fontname', 'PaymentFont,sans-serif')
            if dependency.to_module.is_service:
                node.set('shape', 'hexagon')
            else:
                node.set('shape', 'box')

            if dependency.to_module.is_external:
                node.set('fillcolor', 'lightgreen')
                node.set('style', 'filled')
            graph.add_node(node)

            edge = pydotplus.Edge(dependency.from_instance.__unicode__(), dependency.to_module.__unicode__())
            edge.set('arrowsize', ARROW_SIZE)
            edge.set('fontsize', FONT_SIZE)
            edge.set('fontname', 'PaymentFont,sans-serif')
            if dependency.comment is not None:
                edge.set('xlabel', dependency.comment)
            if dependency.access_direction == READ:
                edge.set('dir', 'back')
            elif dependency.access_direction == BOTH:
                edge.set('dir', 'both')

            if dependency.is_online:
                edge.set('color', 'red')
            elif dependency.is_online is False:
                edge.set('color', 'blue')

            graph.add_edge(edge)
        else:
            filtered_payment_methods = list(set(dependency.payment_methods.iterator()) & set(my_payment_methods))
            if len(filtered_payment_methods) > 0:
                node = pydotplus.Node()
                node.set_name(dependency.to_module.__unicode__())
                node.set('shape', 'box')
                node.set('URL', '/module/%s/' % dependency.to_module.slug)
                node.set('fontsize', FONT_SIZE)
                node.set('fontname', 'PaymentFont,sans-serif')
                if dependency.to_module.is_service:
                    node.set('shape', 'hexagon')
                else:
                    node.set('shape', 'box')

                if dependency.to_module.is_external:
                    node.set('fillcolor', 'lightgreen')
                    node.set('style', 'filled')
                graph.add_node(node)

                edge = pydotplus.Edge(dependency.from_instance.__unicode__(), dependency.to_module.__unicode__())
                edge.set('fontname', 'PaymentFont,sans-serif')
                edge.set('fontsize', FONT_SIZE)
                edge.set('arrowsize', ARROW_SIZE)

                if dependency.access_direction == READ:
                    edge.set('dir', 'back')
                elif dependency.access_direction == BOTH:
                    edge.set('dir', 'both')

                if dependency.is_online:
                    edge.set('color', 'red')
                elif dependency.is_online is False:
                    edge.set('color', 'blue')

                for depending_paynment_method in filtered_payment_methods:
                    if depending_paynment_method.image is not None:
                        label += "%s" % depending_paynment_method.image
                    else:
                        label += "%s" % depending_paynment_method

                if dependency.comment:
                    label = "%s" % (dependency.comment,)

                edge.set('xlabel', label)
                graph.add_edge(edge)


    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph )
    my_graph = re.sub(r"( height=)", " min-height=", my_graph )

    return my_graph