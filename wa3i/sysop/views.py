from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
    }
    return render(request, 'sysop/index.html', context)

def teacher_data(request):
    context = {
    }
    return render(request, 'sysop/teacher_data.html', context)

def quiz_review(request):
    context = {
    }
    return render(request, 'sysop/quiz_review.html', context)

def quiz_produce(request):
    context = {
    }
    return render(request, 'sysop/quiz_produce.html', context)

def quiz_download(request):
    context = {
    }
    return render(request, 'sysop/quiz_download.html', context)

def notice(request):
    context = {
    }
    return render(request, 'sysop/notice.html', context)

def detailed_review(request):
    context = {
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