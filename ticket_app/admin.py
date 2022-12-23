from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Agent, Ticket, company, support_team

admin.site.register(Ticket)
admin.site.register(support_team)
admin.site.register(company)


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('name', 'surname', 'company', 'phone', 'email_address', 'password')
    ordering = ('name',)
    search_fields = ('name', 'email_address')


@admin.register(Agent)
class Agent(admin.ModelAdmin):
    list_display = ('name', 'surname', 'position', 'support_team', 'phone', 'email_address', 'password')
    ordering = ('name',)
    search_fields = ('name', 'email_address')


