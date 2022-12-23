from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField('Name', max_length=120)
    surname = models.CharField('surname', max_length=120)
    company = models.CharField('company', max_length=120)
    phone = models.CharField('Contact Phone', max_length=20)
    email_address = models.EmailField('Email Address', blank=True)
    password = models.CharField('password', max_length=20)


class Agent(models.Model):
    name = models.CharField('Name', max_length=120)
    surname = models.CharField('surname', max_length=120)
    position = models.CharField('position', max_length=120)
    support_team = models.CharField('team', max_length=120)
    phone = models.CharField('Contact Phone', max_length=20)
    email_address = models.EmailField('Email Address', blank=True)
    password = models.CharField('password', max_length=20)


class Ticket(models.Model):

    number = models.IntegerField('number')
    description = models.CharField('description', max_length=120)
    type = models.CharField('type', max_length=120)
    SLA = models.CharField('SLA', max_length=120)
    assigned_to = models.CharField('Agent', max_length=20)
    team = models.CharField('support_team', max_length=120)


class support_team(models.Model):

    name = models.CharField('name', max_length=120)
    scope = models.CharField('scope', max_length=120)
    manager = models.CharField('manager', max_length=120)


class company(models.Model):
    name = models.CharField('name', max_length=120)

