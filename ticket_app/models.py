from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
CHOICES = (
    ('incident', 'INCIDENT'),
    ('major', 'MAJOR'),
)
CATEGORY = (
    ('Server', 'SERVER'),
    ('Client', 'CLIENT'),
    ('Hardware', 'HARDWARE'),
    ('Network', 'NETWORK')
)

SUBCATEGORY1 = (
    ('windows server', 'Windows server'),
    ('unix', 'Unix'),
)
SUBCATEGORY2 = (
    ('windows - system performance', 'WINDOWS - SYSTEM PERFORMANCE'),
    ('Linux - system performance', 'LINUX - SYSTEM PERFORMANCE'),
)
SUBCATEGORY3 = (
    ('printer', 'PRINTER'),
    ('laptop', 'LAPTOP'),
    ('external devices', 'EXTERNAL DEVICES')
)
SUBCATEGORY4 = (
    ('LAN', 'LAN'),
    ('WLAN', 'WLAN'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField('company', max_length=120)
    phone = models.CharField('Contact Phone', max_length=20)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField('position', max_length=120)
    support_team = models.CharField('team', max_length=120)
    phone = models.CharField('Contact Phone', max_length=20)


class Ticket(models.Model):
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    number = models.IntegerField('number')
    description = models.CharField('description', max_length=1000)
    serial_number_or_client_name = models.CharField('serial_number', max_length=1000)
    type = models.CharField('type', choices=CHOICES, max_length=120)
    SLA = models.IntegerField('SLA')
    assigned_to = models.CharField('assigned_to', max_length=20)
    team = models.CharField('support_team', max_length=120)
    status = models.CharField('status', max_length=120)
    comments = models.JSONField('comments', max_length=1000)


class Order(models.Model):

    number = models.IntegerField('number')
    description = models.CharField('description', max_length=1000)
    status = models.CharField('status', max_length=120)


class support_team(models.Model):

    name = models.CharField('name', max_length=120)
    scope = models.CharField('scope', max_length=120)
    manager = models.CharField('manager', max_length=120)
    category = models.CharField('category', choices=CATEGORY, max_length=120)
    subcategory = models.CharField('subcategory', choices=SUBCATEGORY1, max_length=120)


class company(models.Model):
    name = models.CharField('name', max_length=120)

