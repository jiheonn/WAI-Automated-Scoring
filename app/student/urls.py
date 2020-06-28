from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='student'),
    path('AI/', views.AI, name='AI'),
    path('Study/', views.Study, name='Study'),
    path('Homework/', views.Homework, name='Homework'),
    path('Self/', views.Self, name='Self'),
    path('AI/AIques/', views.AIques, name='AIquestion'),
    path('Study/Studyques/', views.Studyques, name='Studyquestion'),
    path('Homework/Homeworkselect/Homeworkcode/Homeworkques/', views.Homeworkques, name='Homeworkquestion'),
    path('Self/Selfques/', views.Selfques, name='Selfquestion'),
    path('Self/Selfques/Selfdiag/', views.Selfdiag, name='Selfdiagnosis'),
    path('Self/Selfques/Selfdiag/Selfgrade/', views.Selfgrade, name='Selfgrade'),
    path('Homework/Homeworkselect/Homeworkcode/Homeworkques/Homeworkdiag/', views.Homeworkdiag,
         name='Homeworkdiagnosis'),
    path('AI/AIques/AIdiag/', views.AIdiag, name='AIdiagnosis'),
    path('Homeworkselect/', views.Homeworkselect, name='Homeworkselect'),
    path('Homeworkselect/Homework/Homeworklist/', views.Homeworklist, name='Homeworklist'),
    path('Homeworkselect/Homework/Homeworklist/Homeworkcheck/', views.Homeworkcheck, name='Homeworkcheck'),
    path('Homeworkselect/Homeworkcode/', views.Homeworkcode, name='Homeworkcode'),
    path('Notice/', views.Notice, name='Notice'),
    path('search/', views.search, name='search'),
    path('search_name/', views.search_name, name='search_name'),
    path('change_category/', views.change_category, name='change_category'),
    path('change_category_self/', views.change_category_self, name='change_category_self'),
    path('check_code/', views.check_code, name='check_code'),
    path('check_ID/', views.check_ID, name='check_ID'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
