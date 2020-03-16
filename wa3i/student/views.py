from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# from .forms import CodeForm


def index(request):
    context = {
    }
    return render(request, 'student/index.html', context)


def AI(request):
    context = {
    }
    return render(request, 'student/AI.html', context)


def Study(request):
    context = {}
    # form = CodeForm(request.POST or None)
    # context['form']= form
    # if request.POST:
    #     if form.is_valid():
    #         temp = form.cleaned_data.get("code_field")
    #         print(type(temp))
    return render(request, 'student/Study.html', context)


def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


def Self(request):
    context = {
    }
    return render(request, 'student/Self.html', context)


def AIques(request):
    context = {
    }
    return render(request, 'student/AIques.html', context)


def Studyques(request):
    context = {
    }
    return render(request, 'student/Studyques.html', context)
