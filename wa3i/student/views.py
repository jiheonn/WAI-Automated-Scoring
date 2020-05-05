from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import q as q
from django.db.models import Q
from mainpage.models import *


def index(request):
    context = {
    }
    return render(request, 'student/index.html', context)


def AI(request):
    qs = Question.objects.all()
    context = {
        'qs': qs
    }
    return render(request, 'student/AI.html', context)


def Study(request):
    context = {}
    return render(request, 'student/Study.html', context)


def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


def Self(request):
    cat = Category.objects.all()
    context = {
        'cat':cat
    }
    return render(request, 'student/Self.html', context)


def AIques(request):
    data = Question.objects.first()

    context = {
        'data': data
    }
    return render(request, 'student/AIques.html', context)


def Studyques(request):
    data = Question.objects.all()
    f = data.first()
    context = {
        'data' : data,
        'f' : f
    }
    return render(request, 'student/Studyques.html', context)


def Studyques2(request):
    context = {
    }
    return render(request, 'student/Studyques2.html', context)


def Homeworkques(request):
    data = Question.objects.first()
    context = {
        'data':data
    }
    return render(request, 'student/Homeworkques.html', context)


def Selfcateg(request):
    data = Keyword.objects.all()
    context = {
        'data': data
    }
    return render(request, 'student/Selfcateg.html', context)


def Selfques(request):
    data = Question.objects.last()
    context = {
        'data': data
    }
    return render(request, 'student/Selfques.html', context)


def Selfdiag(request):
    data = Question.objects.last()
    context = {
        'data': data
    }
    return render(request, 'student/Selfdiag.html', context)


def Selfgrade(request):
    context = {
    }
    return render(request, 'student/Selfgrade.html', context)


def Homeworkdiag(request):
    data = Question.objects.first()
    context = {
        'data':data
    }
    return render(request, 'student/Homeworkdiag.html', context)


def AIdiag(request):
    data = Question.objects.first()

    context = {
        'data': data
    }
    return render(request, 'student/AIdiag.html', context)


def Homeworkselect(request):
    context = {
    }
    return render(request, 'student/Homeworkselect.html', context)


def Homeworklist(request):
    # AssignmentQuestionRel.objects.select_related('Assignment','Solve').values()
    # AssignmentQuestionRel.objects.select_related('Solve').select_related('Assignment').values()
    # rel = AssignmentQuestionRel.objects.select_related('Solve__Assignment').filter(assignment_id='546A5N3Q').values()
    rel = Assignment.objects.prefetch_related('Solve').values()
    # rel = Solve.objects.select_related('Assignment').filter(assignment_id='546A5N3Q').values()

    context = {
        'rel':rel
    }
    return render(request, 'student/Homeworklist.html', context)


def Homeworkcheck(request):
    context = {
    }
    return render(request, 'student/Homeworkcheck.html', context)


def Homeworkcode(request):
    context = {
    }
    return render(request, 'student/Homeworkcode.html', context)


def Searchres(request):
    context = {
    }
    return render(request, 'student/Searchres.html', context)


def Notice(request):
    context = {
    }
    return render(request, 'student/Notice.html', context)


def AIsearch(request):
    data = Question.objects.first()

    context = {
        'data': data
    }
    return render(request, 'student/AIsearch.html', context)
