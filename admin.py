from django.contrib import admin
from instance_manager.models import *
from reversion_compare.admin import CompareVersionAdmin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_group_perms

class instance_conneting_to_instance(admin.TabularInline):
    model = InstanceConnectsInstance
    fk_name = 'from_instance'
    extra = 1

class contacts_for_instance(admin.TabularInline):
    model = InstanceContact
    fk_name = 'parent'
    extra = 1

class instance_connecting_to_module(admin.TabularInline):
    model = InstanceConnectsModule
    fk_name = 'from_instance'
    extra = 1

class LocationAdmin(GuardedModelAdmin, CompareVersionAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class InstanceAdmin(GuardedModelAdmin, CompareVersionAdmin):
    inlines = (contacts_for_instance, instance_conneting_to_instance, instance_connecting_to_module )
    prepopulated_fields = { "slug": ("name",) }

    def get_queryset(self, request):
        qs = super(InstanceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            for object in qs:
                keep = False
                for group in request.user.groups.all():
                    if u'is_owner' in get_group_perms(group, object):
                        keep = True
                if not keep:
                    qs = qs.exclude(pk=object.pk)
            return qs

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            my_group = request.user.groups.all().get(name__contains='TEAM_')
            assign_perm('is_owner', my_group, obj)
admin.site.register(Instance, InstanceAdmin)