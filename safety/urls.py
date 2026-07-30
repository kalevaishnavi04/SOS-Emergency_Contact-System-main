from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add/', views.add_contact, name='add_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('sos/', views.sos_trigger, name='sos'),
]