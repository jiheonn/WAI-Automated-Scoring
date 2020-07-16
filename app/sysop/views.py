from django.shortcuts import render, redirect

# Create your views here.
from mainpage.models import *
from mainpage.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
                messages.error(request, '선생님은 관리자페이지에 접속하실 수 없습니다.')
                return render(request, "sysop/sysop_login.html")
        else:
            messages.error(request, '아이디 또는 비밀번호가 일치하지 않습니다.')
            return render(request, "sysop/sysop_login.html")

    return render(request, "sysop/sysop_login.html")

# 로그아웃 함수
def sysop_logout(request):
    logout(request)
    return redirect("sysop_login")

def home(request):
    context = {
    }
    return render(request, 'sysop/home.html', context)


def teacher_data(request):
    teacher = Teacher.objects.all()
    context = {'teacher':teacher}
    return render(request, 'sysop/teacher_data.html', context)

def change_approve_0_to_1(request):
    teacher_id = request.GET.get('teacher_id')
    teacher_info = Teacher.objects.get(teacher_id=teacher_id)
    teacher_info.approve = 1
    teacher_info.save()
    teacher = Teacher.objects.all()

    context = {'teacher':teacher}
    return render(request, 'sysop/teacher_data.html', context)

def change_approve_1_to_0(request):
    teacher_id = request.GET.get('teacher_id')
    teacher_info = Teacher.objects.get(teacher_id=teacher_id)
    teacher_info.approve = 0
    teacher_info.save()
    teacher = Teacher.objects.all()

    context = {'teacher':teacher}
    return render(request, 'sysop/teacher_data.html', context)

def quiz_review(request):
    makequestion = MakeQuestion.objects.select_related('teacher')
    context = {'makequestion':makequestion
    }
    return render(request, 'sysop/quiz_review.html', context)

def quiz_produce(request):
    question = Question.objects.select_related()
    context = {'question':question
    }
    return render(request, 'sysop/quiz_produce.html', context)

def notice(request):
    context = {
    }
    return render(request, 'sysop/notice.html', context)

def detailed_review(request):
    question_id = request.GET['question_id']
    makequestion = MakeQuestion.objects.select_related('teacher').filter(make_question_id=question_id)[0]
    context = {'makequestion':makequestion
    }
    return render(request, 'sysop/detailed_review.html', context)

def detailed_quiz(request):
    question_id = request.GET.get('question_id')
    question = []
    for i in question_id:
        question = Question.objects.select_related('category').filter(question_id=i)[0]
    context = {'question':question
    }
    return render(request, 'sysop/detailed_quiz.html', context)

def write_quiz(request):
    context = {
    }
    return render(request, 'sysop/write_quiz.html', context)

def ques_review(request):
    question = Question.objects.select_related()
    context = {'question':question
    }
    return render(request, 'sysop/ques_review.html', context)

def ques_detail(request):
    question_id = request.GET.get('question_id')
    question = []
    for i in question_id:
        question = Question.objects.select_related('category').filter(question_id=i)[0]
    context = {'question':question
    }
    return render(request, 'sysop/ques_detail.html', context)

