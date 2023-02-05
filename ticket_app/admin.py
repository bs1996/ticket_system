from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Agent, Ticket, company, support_team, Customer, Category, Subcategory

admin.site.register(Ticket)
admin.site.register(support_team)
admin.site.register(company)


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ('user', 'company', 'phone')
    ordering = ('user',)
    search_fields = ('user',)


@admin.register(Agent)
class Agent(admin.ModelAdmin):
    list_display = ('user', 'position', 'support_team', 'phone')
    ordering = ('user',)
    search_fields = ('user',)


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Subcategory)
class Subcategory(admin.ModelAdmin):
    list_display = ('Category', 'name',)
    ordering = ('name',)
    search_fields = ('name',)
