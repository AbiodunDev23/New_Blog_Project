from django.urls import path
from .import views

urlpatterns = [
    path('logout/', views.custom_logout_views, name='logout'),
    path('logged/', views.logged, name='logged'),
    ]