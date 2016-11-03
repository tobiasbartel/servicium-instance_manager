from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import validate_comma_separated_integer_list

from django.db import models

from servicecatalog.models import STATE, LIVE, ACCESS_DIRECTION, BOTH, PaymentMethod, Module, Contact
from contact_manager.models import Contact, ContactRole

DEV = 'd'
INTE = 'i'
QA = 'q'
CTEST = 'ct'
PROD = 'p'
ENVIRONMENT_OPTIONS = (
    (DEV, 'Development'),
    (INTE, 'Integration'),
    (QA, 'Quality Assurance'),
    (CTEST, 'Customer Test'),
    (PROD, 'Production'),
)

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return str(self.name)

class InstanceConnectsInstance(models.Model):
    from_instance = models.ForeignKey('Instance', related_name='instance_from_relation')
    to_instance = models.ForeignKey('Instance', related_name='instance_to_relation')
    access_direction = models.CharField(choices=ACCESS_DIRECTION, default=BOTH, max_length=2)
    payment_methods = models.ManyToManyField(PaymentMethod, blank=True, default=None)
    comment = models.CharField(max_length=150, default=None, null=True, blank=True)
    is_online = models.NullBooleanField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ('from_instance', 'to_instance', 'access_direction', 'is_online')

    def __unicode__(self):
        return str("%s %s %s" % (self.from_instance, self.get_access_direction_display(), self.to_instance))

class InstanceConnectsModule(models.Model):
    from_instance = models.ForeignKey('Instance', related_name='from_instance_to_module_relation')
    to_module = models.ForeignKey(Module, related_name='to_module_from_instance_relation')
    access_direction = models.CharField(choices=ACCESS_DIRECTION, default=BOTH, max_length=2)
    payment_methods = models.ManyToManyField(PaymentMethod, blank=True, default=None)
    comment = models.CharField(max_length=150, default=None, null=True, blank=True)
    is_online = models.NullBooleanField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ('from_instance', 'to_module', 'access_direction', 'is_online')

    def __unicode__(self):
        return str("%s %s %s" % (self.from_instance, self.get_access_direction_display(), self.to_module.__unicode__))

class Instance(models.Model):
    name = models.CharField(max_length=200, unique=False, blank=True, default='')
    slug = models.SlugField(unique=True, null=True, blank=True)
    module = models.ForeignKey(Module, related_name='instance_of_module')
    environment = models.CharField(max_length=2, choices=ENVIRONMENT_OPTIONS, default=None, blank=False, null=False)
    location = models.ForeignKey('Location', unique=False, blank=None, )
    connected_to_instance = models.ManyToManyField('self', through='InstanceConnectsInstance', symmetrical=False, default=None, blank=True, related_name='instance_on_instance')
    connected_to_module = models.ManyToManyField(Module, through='InstanceConnectsModule', symmetrical=False, default=None, blank=True, related_name='instance_on_module')
    customer_accesable = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE, default=LIVE, blank=False)

    class Meta:
        unique_together = ('name', 'module', 'environment', 'location')
        permissions = (
            ("is_owner", "Is Owner"),
        )

    def __unicode__(self):
        if self.name is not '':
            return str("%s" % (self.name,))
        else:
            return str("%s (%s, %s)" % (self.module.name, self.get_environment_display(), self.location.name))

    def save(self, *args, **kwargs):
        if self.slug == None or len(self.slug) == 0:
            if len(self.name) > 0:
                self.slug = slugify(self.name)
            else:
                self.slug = slugify(self.__unicode__())
        super(Instance, self).save(*args, **kwargs)


class InstanceContact(models.Model):
    parent = models.ForeignKey(Instance)
    contact = models.ForeignKey(Contact)
    role = models.ForeignKey(ContactRole)

    class Meta:
        unique_together = ('parent', 'contact', 'role', )