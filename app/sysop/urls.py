from django.urls import path

from . import views

urlpatterns = [
    # 관리자 홈 페이지
    path("", views.home, name="sysop"),
    # 신규교사정보 페이지
    path("view_teacher_data/", views.view_teacher_data, name="SYS_view_teacher_data"),
    # 문항검토 페이지
    path("view_quiz/", views.view_quiz, name="SYS_view_quiz"),
    path("detail_quiz/", views.detail_quiz, name="SYS_detail_quiz"),
    path("make_quiz/", views.make_quiz, name="SYS_make_quiz"),
    # 문항생성 페이지
    path("view_question/", views.view_question, name="SYS_view_question"),
    path("detail_question/", views.detail_question, name="SYS_detail_question"),
    path("make_question/", views.make_question, name="SYS_make_question"),
    # 함수
    path("sysop_login/", views.sysop_login, name="sysop_login"),
    path("sysop_logout/", views.sysop_logout, name="sysop_logout"),
    path("zero_to_one/", views.zero_to_one, name="SYS_zero_to_one"),
    path("one_to_zero/", views.one_to_zero, name="SYS_one_to_zero"),
    path(
        "create_quiz/",
        views.create_quiz,
        name="SYS_create_quiz"
    ),
    path(
        "create_question/",
        views.create_question,
        name="SYS_create_question"
    ),
    path(
        "change_quiz_info/",
        views.change_quiz_info,
        name="SYS_change_quiz_info"
    ),
    path(
        "change_question_info/",
        views.change_question_info,
        name="SYS_change_question_info"
    ),
    path(
        "delete_question/",
        views.delete_question,
        name="SYS_delete_question"
    ),
]
