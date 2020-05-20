from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('introduce', views.introduce, name='introduce'),
    path('handbook', views.handbook, name='handbook'),
]