from django.shortcuts import render, redirect

# Create your views here.
from mainpage.models import *
from mainpage.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

APPROVED = 0

@method_decorator(csrf_exempt)
def sysop_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.username == "admin":
                login(request, user)
                return render(request, "sysop/home.html")
            else:
                messages.error(request, "선생님은 관리자페이지에 접속하실 수 없습니다.")
                return render(request, "sysop/sysop_login.html")
        else:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "sysop/sysop_login.html")

    return render(request, "sysop/sysop_login.html")


# 로그아웃 함수
def sysop_logout(request):
    logout(request)
    return redirect("sysop_login")


def home(request):
    context = {}
    return render(request, "sysop/home.html", context)


def teacher_data(request):
    teacher = Teacher.objects.all()
    context = {"teacher": teacher}
    return render(request, "sysop/teacher_data.html", context)


def change_approve_0_to_1(request):
    if request.method == "GET" and "teacher_id" in request.GET:
        teacher_id = request.GET.get("teacher_id")
        teacher_info = Teacher.objects.get(teacher_id=teacher_id)
        teacher_info.approve = 1
        teacher_info.save()
        teacher = Teacher.objects.all()

        context = {"teacher": teacher}
        return render(request, "sysop/teacher_data.html", context)

    elif request.method == "GET" and "make_question_id" in request.GET:
        make_question_id = request.GET.get("make_question_id")
        make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
        make_question_info.upload_check = 1 #TODO : Use meaningful name
        make_question_info.save()
        make_question = MakeQuestion.objects.all()

        context = {"makequestion": make_question}
        return render(request, "sysop/quiz_review.html", context)

#TODO Rename function : change_approve_1_to_0 --> one_to_zero
def change_approve_1_to_0(request):
    if request.method == "GET" and "teacher_id" in request.GET:
        teacher_id = request.GET.get("teacher_id")
        teacher_info = Teacher.objects.get(teacher_id=teacher_id)
        teacher_info.approve = APPROVED #TODO : Use meaningful name
        teacher_info.save()
        teacher = Teacher.objects.all()

        context = {"teacher": teacher}
        return render(request, "sysop/teacher_data.html", context)

    elif request.method == "GET" and "make_question_id" in request.GET:
        make_question_id = request.GET.get("make_question_id")
        make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
        make_question_info.upload_check = 0 #TODO : Use meaningful name
        make_question_info.save()
        make_question = MakeQuestion.objects.all()

        context = {"makequestion": make_question}
        return render(request, "sysop/quiz_review.html", context)


def quiz_review(request):
    makequestion = MakeQuestion.objects.all()
    context = {"makequestion": makequestion}
    return render(request, "sysop/quiz_review.html", context)


def detailed_review(request):
    question_id = request.GET["question_id"]
    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=question_id
    )[0] #TODO : What is the meaning of the [0] -> make function or menaningful index
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}
    return render(request, "sysop/detailed_review.html", context)


def change_self_question_info(request):
    self_question_id = request.GET.get("self_question_id")
    self_question_info = MakeQuestion.objects.get(make_question_id=self_question_id)
    self_question_info.question_name = request.GET.get("self_question_name")
    self_question_info.discription = request.GET.get("self_question_discription")
    self_question_info.answer = request.GET.get("self_question_answer")
    self_question_info.hint = request.GET.get("self_question_hint")
    self_question_info.save()

    mark_text_list = request.GET.getlist("self_question_mark")
    mark_data_list = Mark.objects.select_related("make_question").filter(
        make_question_id=self_question_id
    )

    # TODO: What are i and j? --> Use meaningful variable name
    for i, j in zip(mark_text_list, mark_data_list):
        mark_data = Mark.objects.get(mark_id=j.mark_id)
        mark_data.mark_text = i
        mark_data.save()

    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=self_question_id
    )[0] # TODO
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=self_question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}
    return render(request, "sysop/detailed_review.html", context)


def write_quiz(request):
    context = {}
    return render(request, "sysop/write_quiz.html", context)


def create_self_question(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        teacher_id = 0 #TODO: why 0? TEACHER_ADMIN = 0
        make_question_data = MakeQuestion(
            teacher=Teacher.objects.get(teacher_id=teacher_id),
            question_name=request.POST["question_name"],
            discription=request.POST["discription"],
            answer=request.POST["answer"],
            image=request.FILES["image"],
            hint=request.POST["hint"],
            made_date=now_date,
            upload_check=0, #TODO : use meaningful variable
        )
        make_question_data.save()

        mark_list = request.POST.getlist("mark_text")
        temp = MakeQuestion.objects.get(hint=request.POST["hint"], made_date=now_date)
        # MakeQuestion Table 과 연결된 Mark Table 데이터 추가
        for i in mark_list:
            mark_data = Mark(mark_text=i, make_question_id=temp.make_question_id)
            mark_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("write_quiz")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("write_quiz")


def quiz_produce(request):
    question = Question.objects.select_related()
    context = {"question": question}
    return render(request, "sysop/quiz_produce.html", context)


def notice(request):
    context = {}
    return render(request, "sysop/notice.html", context)


def detailed_quiz(request):
    question_id = request.GET.get("question_id")
    question = []
    for i in question_id:
        question = Question.objects.select_related("category").filter(question_id=i)[0]
    context = {"question": question}
    return render(request, "sysop/detailed_quiz.html", context)


def ques_review(request):
    question = Question.objects.select_related()
    context = {"question": question}
    return render(request, "sysop/ques_review.html", context)


def ques_detail(request):
    question_id = request.GET.get("question_id")
    question = []
    for i in question_id:
        question = Question.objects.select_related("category").filter(question_id=i)[0]
    context = {"question": question}
    return render(request, "sysop/ques_detail.html", context)
