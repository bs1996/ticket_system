from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
CHOICES = (
    ('incident', 'INCIDENT'),
    ('major', 'MAJOR'),
)

CATEGORY = [
    ('Server', (
            ('Windows server', 'Windows server'),
            ('Unix', 'Unix'),
        )
    ),
    ('Client', (
            ('Windows - system performance', 'Windows - system performance'),
            ('Linux - system performance', 'Linux - system performance'),
        )
    ),
    ('Hardware', (
            ('printer', 'printer'),
            ('laptop', 'laptop'),
        )
    ),
    ('Network', 'Network'),]



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
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    number = models.IntegerField('number')
    description = models.CharField('description', max_length=1000)
    status = models.CharField('status', max_length=120)
    category = models.CharField('category', null=True, max_length=120)


class Category(models.Model):
    name = models.CharField('name', max_length=120)

    def _str_(self):
        return self.name


class Subcategory(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=120)

    def _str_(self):
        return self.name


class support_team(models.Model):
    name = models.CharField('name', max_length=120)
    scope = models.CharField('scope', max_length=120)
    manager = models.CharField('manager', max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.OneToOneField(Subcategory, on_delete=models.CASCADE)

    def _str_(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField('position', max_length=120)
    support_team = models.ForeignKey(support_team, on_delete=models.CASCADE)
    phone = models.CharField('Contact Phone', max_length=20)


class company(models.Model):
    name = models.CharField('name', max_length=120)


class screenshots(models.Model):
    Ticket = models.ForeignKey(Ticket, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    ticket_numb = models.CharField('ticket_numb', max_length=120)



