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
    path('Homework/Homeworkselect/Homeworkcode/Homeworkques/', views.Homeworkques, name='Homeworkquestion'),
    path('Self/Selfcateg/', views.Selfcateg, name='Selfcategory'),
    path('Self/Selfcateg/Selfques/', views.Selfques, name='Selfquestion'),
    path('Self/Selfcateg/Selfques/Selfdiag/', views.Selfdiag, name='Selfdiagnosis'),
    path('Self/Selfcateg/Selfques/Selfdiag/Selfgrade/', views.Selfgrade, name='Selfgrade'),
    path('Homework/Homeworkselect/Homeworkcode/Homeworkques/Homeworkdiag/', views.Homeworkdiag, name='Homeworkdiagnosis'),
    path('AI/AIques/AIdiag/', views.AIdiag, name='AIdiagnosis'),
    path('Homework/Homeworkselect/', views.Homeworkselect, name='Homeworkselect'),
    path('Homework/Homeworkselect/Homeworkcheck/', views.Homeworkcheck, name='Homeworkcheck'),
    path('Homework/Homeworkselect/Homeworkcode/', views.Homeworkcode, name='Homeworkcode'),
    path('Self/Searchres/', views.Searchres, name='Searchresult'),
    path('Notice/', views.Notice, name='Notice'),
]