from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='student'),
    path('AI/', views.AI, name='AI'),
    path('Study/', views.Study, name='Study'),
    path('Homework/', views.Homework, name='Homework'),
    path('Self/', views.Self, name='Self'),
    path('AI/AIques/', views.AIques, name='AIquestion'),
    path('Study/Studyques/', views.Studyques, name='Studyquestion'),
    path('Homework/Homeworkques/', views.Homeworkques, name='Homeworkquestion'),
    path('Self/Selfcateg/', views.Selfcateg, name='Selfcategory'),
    path('Self/Selfcateg/Selfques/', views.Selfques, name='Selfquestion'),
    path('Self/Selfcateg/Selfques/Selfdiag/', views.Selfdiag, name='Selfdiagnosis'),
    path('Self/Selfcateg/Selfques/Selfdiag/Selfgrade/', views.Selfgrade, name='Selfgrade'),
    path('Homework/Homeworkques/Homeworkdiag/', views.Homeworkdiag, name='Homeworkdiagnosis'),
    path('AI/AIques/AIdiag', views.AIdiag, name='AIdiagnosis'),
]