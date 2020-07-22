from django.shortcuts import render, redirect

# Create your views here.
from mainpage.models import *
from mainpage.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

APPROVED_ALLOW = 1
APPROVED_DENY = 0


# 관리자 홈 페이지
def home(request):
    context = {}
    return render(request, "sysop/home.html", context)


# 신규교사정보 페이지
def teacher_data(request):
    teacher = Teacher.objects.all()
    context = {"teacher": teacher}
    return render(request, "sysop/teacher_data.html", context)


# 문항검토 페이지
def quiz(request):
    makequestion = MakeQuestion.objects.all()
    context = {"makequestion": makequestion}
    return render(request, "sysop/quiz.html", context)


# 문항검토 자세히보기 페이지
def detail_quiz(request):
    question_id = request.GET["question_id"]
    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=question_id
    ).first()
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}
    return render(request, "sysop/detail_quiz.html", context)


# 문항검토 신규문항 생성 페이지
def make_quiz(request):
    context = {}
    return render(request, "sysop/make_quiz.html", context)


# 문항생성 페이지
def question(request):
    question = Question.objects.all()
    context = {"question": question}
    return render(request, "sysop/question.html", context)


# 문항생성 자세히보기 페이지
def detail_question(request):
    question_id = request.GET["question_id"]
    question = Question.objects.filter(question_id=question_id).first()
    category = Category.objects.all()

    context = {"question": question,
               "category": category}
    return render(request, "sysop/detail_question.html", context)


# 문항검토 신규문항 생성 페이지
def make_question(request):
    category = Category.objects.all()

    context = {"category": category, }
    return render(request, "sysop/make_question.html", context)


# 로그인 함수
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


# 등록하기 함수
def zero_to_one(request):
    if request.method == "GET" and "teacher_id" in request.GET:
        teacher_id = request.GET.get("teacher_id")
        teacher_info = Teacher.objects.get(teacher_id=teacher_id)
        teacher_info.approve = APPROVED_ALLOW
        teacher_info.save()
        teacher = Teacher.objects.all()

        context = {"teacher": teacher}
        return render(request, "sysop/teacher_data.html", context)

    elif request.method == "GET" and "make_question_id" in request.GET:
        make_question_id = request.GET.get("make_question_id")
        make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
        make_question_info.upload_check = APPROVED_ALLOW
        make_question_info.save()
        make_question = MakeQuestion.objects.all()

        context = {"makequestion": make_question}
        return render(request, "sysop/quiz.html", context)


# 취소하기 함수
def one_to_zero(request):
    if request.method == "GET" and "teacher_id" in request.GET:
        teacher_id = request.GET.get("teacher_id")
        teacher_info = Teacher.objects.get(teacher_id=teacher_id)
        teacher_info.approve = APPROVED_DENY
        teacher_info.save()
        teacher = Teacher.objects.all()

        context = {"teacher": teacher}
        return render(request, "sysop/teacher_data.html", context)

    elif request.method == "GET" and "make_question_id" in request.GET:
        make_question_id = request.GET.get("make_question_id")
        make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
        make_question_info.upload_check = APPROVED_DENY
        make_question_info.save()
        make_question = MakeQuestion.objects.all()

        context = {"makequestion": make_question}
        return render(request, "sysop/quiz.html", context)


# 문항검토 신규문항 생성 함수
def create_quiz(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        TEACHER_ADMIN = 0

        image_number = MakeQuestion.objects.all().last().make_question_id + 1
        image = request.FILES["image"]
        image.name = str(image_number) + "_" + image.name

        make_question_data = MakeQuestion(
            teacher=Teacher.objects.get(teacher_id=TEACHER_ADMIN),
            question_name=request.POST["question_name"],
            discription=request.POST["discription"],
            answer=request.POST["answer"],
            image=image,
            hint=request.POST["hint"],
            made_date=now_date,
            upload_check=APPROVED_DENY,
        )

        make_question_data.save()
        mark_list = request.POST.getlist("mark_text")

        # MakeQuestion Table 과 연결된 Mark Table 데이터 추가
        for mark_text in mark_list:
            mark_change_data = Mark(mark_text=mark_text, make_question_id=make_question_data.make_question_id)
            mark_change_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("make_quiz")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("make_quiz")


# 문항생성 신규문항 생성 함수
def create_question(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    image_number = MakeQuestion.objects.all().last().make_question_id + 1
    image = request.FILES["image"]
    image.name = str(image_number) + "_" + image.name

    try:
        question_data = Question(
            category=Category.objects.filter(category_id=request.POST["question_category_id"]).first(),
            model_id=1,
            question_name=request.POST["question_name"],
            discription=request.POST["question_discription"],
            answer=request.POST["question_answer"],
            image=image,
            hint=request.POST["question_hint"],
            made_date=now_date,
            qr_code="qr_code/image/qr_code.png",
            ques_concept=request.POST["question_concept"],
        )
        question_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("make_question")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("make_question")


# 문항검토 수정 함수
def change_quiz_info(request):
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

    for mark_text, mark_data in zip(mark_text_list, mark_data_list):
        mark_change_data = Mark.objects.get(mark_id=mark_data.mark_id)
        mark_change_data.mark_text = mark_text
        mark_change_data.save()

    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=self_question_id
    ).first()
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=self_question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}
    return render(request, "sysop/detail_quiz.html", context)


# 문항생성 정보 수정 함수
def change_question_info(request):
    question_id = request.GET.get("question_id")
    question_info = Question.objects.get(question_id=question_id)
    question_info.question_name = request.GET.get("question_name")
    question_info.category = Category.objects.filter(category_id=request.GET.get("question_category_id")).first()
    question_info.ques_concept = request.GET.get("question_concept")
    question_info.discription = request.GET.get("question_discription")
    question_info.answer = request.GET.get("question_answer")
    question_info.hint = request.GET.get("question_hint")
    question_info.save()

    question = Question.objects.filter(question_id=question_id).first()
    category = Category.objects.all()

    context = {"question": question,
               "category": category}
    return render(request, "sysop/detail_question.html", context)