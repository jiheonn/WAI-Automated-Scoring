from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 좋은 설명 페이지
    path("", views.good_explain, name="student"),
    path("AI/", views.ai, name="AI"),
    path("AI/AIques/", views.ai_question, name="AIquestion"),
    path("AI/AIques/AIdiag/", views.ai_diagnosis, name="AIdiagnosis"),
    path("Study/", views.study_evaluate, name="Study"),
    path("Study/Studyques/", views.study_evaluate_question, name="Studyquestion"),
    path("Homeworkselect/", views.homework_do_check_select, name="Homeworkselect"),
    path("Homework/", views.homework_check_id, name="Homework"),
    path(
        "Homeworkselect/Homework/Homeworklist/", views.homework_check_list, name="Homeworklist"
    ),
    path(
        "Homeworkselect/Homework/Homeworklist/Homeworkcheck/",
        views.homework_check_homework,
        name="Homeworkcheck",
    ),
    path("Homeworkselect/Homeworkcode/", views.homework_do_code, name="Homeworkcode"),
    path(
        "Homework/Homeworkselect/Homeworkcode/Homeworkques/",
        views.homework_do_question,
        name="Homeworkquestion",
    ),
    path(
        "Homework/Homeworkselect/Homeworkcode/Homeworkques/Homeworkdiag/",
        views.homework_do_diagnosis,
        name="Homeworkdiagnosis",
    ),
    path("Self/", views.self, name="Self"),
    path("Self/Selfques/", views.self_question, name="Selfquestion"),
    path("Self/Selfques/Selfdiag/", views.self_diagnosis, name="Selfdiagnosis"),
    path("Self/Selfques/Selfdiag/Selfgrade/", views.self_grade_score, name="Selfgrade"),
    path("Notice/", views.notice, name="Notice"),
    path("search/", views.search_keyword, name="search"),
    path("search_name/", views.search_name, name="search_name"),
    path("change_category/", views.change_category_ai, name="change_category"),
    # path(
    #     "change_category_self/", views.change_category_self, name="change_category_self"
    # ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)