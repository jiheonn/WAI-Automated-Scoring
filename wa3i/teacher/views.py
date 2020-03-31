from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
    }
    return render(request, 'teacher/index.html', context)


def question_selection(request):
    context = {
    }
    return render(request, 'teacher/question_selection.html', context)


def view_result(request):
    context = {
    }
    return render(request, 'teacher/view_result.html', context)


def make_question(request):
    context = {
    }
    return render(request, 'teacher/make_question.html', context)


def bigram_tree(request):
    context = {
    }
    return render(request, 'teacher/bigram_tree.html', context)


def topic_analysis(request):
    context = {
    }
    return render(request, 'teacher/topic_analysis.html', context)


def response_analysis(request):
    context = {
    }
    return render(request, 'teacher/response_analysis.html', context)


def qr_code(request):
    context = {
    }
    return render(request, 'teacher/QR_code.html', context)


def notice(request):
    context = {
    }
    return render(request, 'teacher/notice.html', context)


def ex_view_result(request):
    context = {
    }
    return render(request, 'teacher/ex_view_result.html', context)


def ex_response_analysis(request):
    context = {
    }
    return render(request, 'teacher/ex_response_analysis.html', context)
