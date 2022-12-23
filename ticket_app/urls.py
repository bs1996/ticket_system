from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.login),
   # path('contact/', views.contact),
    path('home/', views.index, name='home'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    # path('settings/', include(views.settings)),

]