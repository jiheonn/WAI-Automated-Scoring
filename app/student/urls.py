from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 좋은 설명 페이지
    path("", views.good_explain, name="student"),
    # 평가연습 페이지
    path(
        "evaluate_exercise/", views.evaluate_exercise, name="student_evaluate_exercise"
    ),
    path(
        "evaluate_exercise/question/",
        views.evaluate_exercise_question,
        name="student_evaluate_exercise_question",
    ),
    path(
        "evaluate_exercise/question/diagnosis/",
        views.evaluate_exercise_diagnosis,
        name="student_evaluate_exercise_diagnosis",
    ),
    # 학습평가 페이지
    path("study_evaluate/", views.study_evaluate, name="student_study_evaluate"),
    path(
        "study_evaluate/question/",
        views.study_evaluate_question,
        name="student_study_evaluate_question",
    ),
    # 숙제하기, 숙제 조회 중 선택 페이지
    path("select_homework/", views.select_homework, name="student_select_homework"),
    # 숙제 조회 페이지
    path(
        "check_homework_by_id/",
        views.check_homework_by_id,
        name="student_check_homework_by_id",
    ),
    path(
        "check_homework_list/",
        views.check_homework_list,
        name="student_check_homework_list",
    ),
    path(
        "check_homework_list/check_homework_question",
        views.check_homework_question,
        name="student_check_homework_question",
    ),
    # 숙제하기 페이지
    path(
        "do_homework_by_code/",
        views.do_homework_by_code,
        name="student_do_homework_by_code",
    ),
    path(
        "do_homework/question/",
        views.do_homework_question,
        name="student_do_homework_question",
    ),
    path(
        "do_homework/question/diagnosis/",
        views.do_homework_diagnosis,
        name="student_do_homework_diagnosis",
    ),
    # 스스로 평가 페이지
    path("evaluate_by_self/", views.evaluate_by_self, name="student_evaluate_by_self"),
    path(
        "evaluate_by_self/question/",
        views.evaluate_by_self_question,
        name="student_evaluate_by_self_question",
    ),
    path(
        "evaluate_by_self/question/diagnosis/",
        views.evaluate_by_self_diagnosis,
        name="student_evaluate_by_self_diagnosis",
    ),
    path(
        "evaluate_by_self/question/diagnosis/score/",
        views.evaluate_by_self_score,
        name="student_evaluate_by_self_score",
    ),
    # 게시판 페이지
    path("notice/", views.notice, name="student_notice"),
    # 함수
    path("search/", views.search_keyword, name="search"),
    path("search_name/", views.search_name, name="search_name"),
    path(
        "change_category/",
        views.change_category_evaluate_exercise,
        name="change_category",
    ),
    # path(
    #     "change_category_self/", views.change_category_self, name="change_category_self"
    # ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
