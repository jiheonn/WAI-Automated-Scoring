from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="teacher"),
    path(
        "question_selection/",
        views.question_selection,
        name="teacher_question_selection",
    ),
    path("view_result/", views.view_result, name="teacher_view_result"),
    path("make_question/", views.make_question, name="teacher_make_question"),
    path("bigram_tree/", views.bigram_tree, name="teacher_bigram_tree"),
    path("topic_analysis/", views.topic_analysis, name="teacher_topic_analysis"),
    path(
        "response_analysis/", views.response_analysis, name="teacher_response_analysis"
    ),
    path("qr_code/", views.qr_code, name="teacher_qr_code"),
    path("notice/", views.teacher_notice, name="teacher_notice"),
    path(
        "view_result/view_result_detail/",
        views.view_result_detail,
        name="teacher_view_result_detail",
    ),
    path("change_qr_code/", views.change_qr_code, name="teacher_change_qr_code"),
    path("question_search/", views.question_search, name="teacher_question_search"),
    path("assignment_copy/", views.assignment_copy, name="teacher_assignment_copy"),
    path("change_category/", views.change_category, name="teacher_change_category"),
    path("code_generation/", views.code_generation, name="teacher_code_generation"),
    path("login/", views.login_view, name="teacher_login"),
    path("logout/", views.logout_view, name="teacher_logout"),
    path("signup/", views.signup_view, name="teacher_signup"),
    path("view_result/view_result_detail/chart/", views.chart, name="teacher_chart"),
    path(
        "question_selection_save/",
        views.question_selection_save,
        name="teacher_question_selection_save",
    ),
    path(
        "make_question_save/",
        views.make_question_save,
        name="teacher_make_question_save",
    ),
]
