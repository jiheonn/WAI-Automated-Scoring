from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from mainpage.models import *


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
    }
    return render(request, 'sysop/index.html', context)

def teacher_data(request):
    if request.GET.get('evaluation_type'):
        featured_filter = request.GET.get('evaluation_type')
        teacher = Teacher.objects.filter()
    else:
        teacher = Teacher.objects.all()

    context = {'teacher':teacher}
    return render(request, 'sysop/teacher_data.html', context)

def quiz_review(request):
    makequestion = MakeQuestion.objects.select_related('teacher')
    context = {'makequestion':makequestion
    }
    return render(request, 'sysop/quiz_review.html', context)

def quiz_produce(request):
    makequestion = MakeQuestion.objects.select_related('teacher')
    context = {'makequestion':makequestion
    }
    return render(request, 'sysop/quiz_produce.html', context)

def quiz_download(request):
    makequestion = MakeQuestion.objects.all()
    question = Question.objects.select_related('category')
    context = {'makequestion':makequestion, 'question':question
    }
    return render(request, 'sysop/quiz_download.html', context)

def notice(request):
    context = {
    }
    return render(request, 'sysop/notice.html', context)

def detailed_review(request):
    makequestion = MakeQuestion.objects.all()
    context = {'makequestion':makequestion
    }
    return render(request, 'sysop/detailed_review.html', context)

def detailed_quiz(request):
    context = {
    }
    return render(request, 'sysop/detailed_quiz.html', context)

def detailed_download(request):
    context = {
    }
    return render(request, 'sysop/detailed_download.html', context)

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
    context = {
    }
    return render(request, 'sysop/ques_detail.html', context)

