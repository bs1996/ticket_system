from django.urls import path, include
from . import views
from .views import register
urlpatterns = [
    path('all_tickets/', views.all_tickets),
    path('mytickets/incident_user/<int:number>', views.incident_user),
    path('all_tickets/incident_agent/<int:number>', views.incident_agent),
    path('mytickets/incident_agent/<int:number>', views.incident_agent),
    path('mytickets/', views.my_tickets),
    path('login/', views.sign_in),
    path('signout/', views.signout),
    path('contact/', views.contact),
    path('create_ticket/', views.create_ticket),
    path('order/', views.order),
    # path('contact/', views.contact),
    path('home/', views.index, name='home'),
    path('', views.index, name='index'),
    path('register/', register, name='signup'),
    # path('settings/', include(views.settings)),

]