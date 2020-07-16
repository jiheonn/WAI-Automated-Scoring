from django.urls import path

from . import views

urlpatterns = [
    path('sysop_login/', views.sysop_login, name='sysop_login'),
    path('sysop_logout/', views.sysop_logout, name='sysop_logout'),
    path('', views.home, name='sysop'),
    path('teacher_data/', views.teacher_data, name='teacher_data'),
    path('change_approve_0_to_1/', views.change_approve_0_to_1, name='change_approve_0_to_1'),
    path('change_approve_1_to_0/', views.change_approve_1_to_0, name='change_approve_1_to_0'),
    path('quiz_review/', views.quiz_review, name='quiz_review'),
    path('quiz_produce/', views.quiz_produce, name='quiz_produce'),
    path('notice/', views.notice, name='notice'),
    path('detailed_review/', views.detailed_review, name='detailed_review'),
    path('detailed_quiz/', views.detailed_quiz, name='detailed_quiz'),
    path('write_quiz/', views.write_quiz, name='write_quiz'),
    path('ques_detail/', views.ques_detail, name='ques_detail')
]