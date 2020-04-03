from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='teacher'),
    path('question_selection/', views.question_selection, name='question_selection'),
    path('view_result/', views.view_result, name='view_result'),
    path('make_question/', views.make_question, name='make_question'),
    path('bigram_tree/', views.bigram_tree, name='bigram_tree'),
    path('topic_analysis/', views.topic_analysis, name='topic_analysis'),
    path('response_analysis/', views.response_analysis, name='response_analysis'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('notice/', views.teacher_notice, name='teacher_notice'),
    path('view_result/ex_view_result/', views.ex_view_result, name='ex_view_result'),
    path('response_analysis/ex_response_analysis/', views.ex_response_analysis, name='ex_response_analysis'),
]