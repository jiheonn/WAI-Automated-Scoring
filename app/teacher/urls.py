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
    path('change_qr_code/', views.change_qr_code, name='change_qr_code'),
    path('question_search/', views.question_search, name='question_search'),
    path('assignment_copy/', views.assignment_copy, name='assignment_copy'),
    path('change_category/', views.change_category, name='change_category'),
    path('code_generation/', views.code_generation, name='code_generation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('view_result/view_result_detail/chart/', views.chart, name='chart'),
    path('question_selection_save/', views.question_selection_save, name='question_selection_save'),
    path('make_question_save/', views.make_question_save, name='make_question_save'),
]
