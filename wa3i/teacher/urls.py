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
    path('view_result/view_result_detail/', views.view_result_detail, name='view_result_detail'),
    path('response_analysis/ex_response_analysis/', views.ex_response_analysis, name='ex_response_analysis'),
    # path('view_result_detail/', views.view_result_detail, name='view_result_detail'),
    path('change_qr_code/', views.change_qr_code, name='change_qr_code'),
    path('question_search/', views.question_search, name='question_search'),
    path('view_search/', views.view_search, name='view_search'),
    path('assignment_copy/', views.assignment_copy, name='assignment_copy'),
    path('change_category/', views.change_category, name='change_category'),
]