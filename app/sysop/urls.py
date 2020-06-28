from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='sysop'),
    path('teacher_data/', views.teacher_data, name='teacher_data'),
    path('quiz_review/', views.quiz_review, name='quiz_review'),
    path('quiz_produce/', views.quiz_produce, name='quiz_produce'),
    path('notice/', views.notice, name='notice'),
    path('detailed_review/', views.detailed_review, name='detailed_review'),
    path('detailed_quiz/', views.detailed_quiz, name='detailed_quiz'),
    path('write_quiz/', views.write_quiz, name='write_quiz'),
    path('ques_review/', views.ques_review, name='ques_review'),
    path('ques_detail/', views.ques_detail, name='ques_detail')
]