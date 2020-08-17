from django.urls import path

from . import views

urlpatterns = [
    # 관리자 홈 페이지
    path("", views.home, name="sysop"),
    # 신규교사정보 페이지
    path("view_teacher_data/", views.view_teacher_data, name="sysop_view_teacher_data"),
    # 문항검토 페이지
    path("view_quiz/", views.view_quiz, name="sysop_view_quiz"),
    path("detail_quiz/", views.detail_quiz, name="sysop_detail_quiz"),
    path("make_quiz/", views.make_quiz, name="sysop_make_quiz"),
    # 문항생성 페이지
    path("view_question/", views.view_question, name="sysop_view_question"),
    path("detail_question/", views.detail_question, name="sysop_detail_question"),
    path("make_question/", views.make_question, name="sysop_make_question"),
    # 공지사항 페이지
    path("view_notice/", views.view_notice, name="sysop_view_notice"),
    path("detail_notice/", views.detail_notice, name="sysop_detail_notice"),
    path("make_notice/", views.make_notice, name="sysop_make_notice"),
    # 함수
    path("sysop_login/", views.sysop_login, name="sysop_login"),
    path("sysop_logout/", views.sysop_logout, name="sysop_logout"),
    path(
        "deny_to_allow_teacher_approve/",
        views.deny_to_allow_teacher_approve,
        name="sysop_deny_to_allow_teacher_approve"
    ),
    path(
        "allow_to_deny_teacher_approve/",
        views.allow_to_deny_teacher_approve,
        name="sysop_allow_to_deny_teacher_approve"
    ),
    path(
        "deny_to_allow_quiz/",
        views.deny_to_allow_quiz,
        name="sysop_deny_to_allow_quiz"
    ),
    path(
        "allow_to_deny_quiz/",
        views.allow_to_deny_quiz,
        name="sysop_allow_to_deny_quiz"
    ),
    path(
        "create_quiz/",
        views.create_quiz,
        name="sysop_create_quiz"
    ),
    path(
        "create_question/",
        views.create_question,
        name="sysop_create_question"
    ),
    path(
        "create_notice/",
        views.create_notice,
        name="sysop_create_notice"
    ),
    path(
        "change_quiz_info/",
        views.change_quiz_info,
        name="sysop_change_quiz_info"
    ),
    path(
        "change_question_info/",
        views.change_question_info,
        name="sysop_change_question_info"
    ),
    path(
        "change_notice_info/",
        views.change_notice_info,
        name="sysop_change_notice_info"
    ),
    path(
        "delete_question/",
        views.delete_question,
        name="sysop_delete_question"
    ),
    path(
        "delete_notice/",
        views.delete_notice,
        name="sysop_delete_notice"
    ),
]
