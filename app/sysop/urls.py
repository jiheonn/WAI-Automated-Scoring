from django.urls import path

from . import views

urlpatterns = [
    # 관리자 홈 페이지
    path("", views.home, name="sysop"),
    # 신규교사정보 페이지
    path("teacher_data/", views.teacher_data, name="teacher_data"),
    # 문항검토 페이지
    path("quiz/", views.quiz, name="quiz"),
    path("detail_quiz/", views.detail_quiz, name="detail_quiz"),
    path("make_quiz/", views.make_quiz, name="make_quiz"),
    # 문항생성 페이지
    path("question/", views.question, name="question"),
    path("detail_question/", views.detail_question, name="detail_question"),
    path("make_question/", views.make_question, name="make_question"),
    # 함수
    path("sysop_login/", views.sysop_login, name="sysop_login"),
    path("sysop_logout/", views.sysop_logout, name="sysop_logout"),
    path("zero_to_one/", views.zero_to_one, name="zero_to_one"),
    path("one_to_zero/", views.one_to_zero, name="one_to_zero"),
    path(
        "create_quiz/",
        views.create_quiz,
        name="create_quiz"
    ),
    path(
        "create_question/",
        views.create_question,
        name="create_question"
    ),
    path(
        "change_quiz_info/",
        views.change_quiz_info,
        name="change_quiz_info"
    ),
    path(
        "change_question_info/",
        views.change_question_info,
        name="change_question_info"
    ),
    path(
        "delete_question/",
        views.delete_question,
        name="delete_question"
    ),
]
