from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from mainpage.models import *
from django.http import JsonResponse
from mainpage.models import *

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
    }
    return render(request, 'sysop/index.html', context)

def teacher_data(request):
    teacher_id = request.GET.get('teacher_id')
    # print(teacher)
    if teacher_id == None:
        teacher = Teacher.objects.all()
    else:
        teacher_info = Teacher.objects.get(teacher_id=teacher_id)
        teacher_info.approve = 1
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

