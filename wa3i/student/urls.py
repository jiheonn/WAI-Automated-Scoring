from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='student'),
    path('AI/', views.AI, name='AI'),
    path('Study/', views.Study, name='Study'),
    path('Homework/', views.Homework, name='Homework'),
    path('Self/', views.Self, name='Self'),
    path('AI/AIques', views.AIques, name='AIquestion'),
    path('Study/Studyques', views.Studyques, name='Studyquestion'),
]