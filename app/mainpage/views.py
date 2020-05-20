from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {
    }
    return render(request, 'mainpage/index.html', context)


def introduce(request):
    context = {
    }
    return render(request, 'mainpage/introduce.html', context)

def handbook(request):
    context = {
    }
    return render(request, 'mainpage/handbook.html', context)