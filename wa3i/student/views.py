from builtins import dict

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import q as q
from django.db.models import Q
from django.http import JsonResponse

from mainpage.models import Question, SelfSolveData, AssignmentQuestionRel, Keyword, Solve, Assignment


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
    context = {

    }
    return render(request, 'student/Study.html', context)


def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


def Self(request):
    qs = Question.objects.all()
    context = {
        'qs': qs
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


def Selfques(request):
    data = Question.objects.last()
    context = {
        'data': data
    }
    return render(request, 'student/Selfques.html', context)


def Selfdiag(request):
    data = SelfSolveData.objects.select_related('make_question').last()
    context = {
        'data': data
    }
    return render(request, 'student/Selfdiag.html', context)


def Selfgrade(request):
    context = {
    }
    return render(request, 'student/Selfgrade.html', context)


def Homeworkdiag(request):
    data = AssignmentQuestionRel.objects.select_related('question','solve').first()
    context = {
        'data':data
    }
    return render(request, 'student/Homeworkdiag.html', context)


def AIdiag(request):
    data = AssignmentQuestionRel.objects.select_related('question','solve').first()

    context = {
        'data': data
    }
    return render(request, 'student/AIdiag.html', context)


def Homeworkselect(request):
    context = {
    }
    return render(request, 'student/Homeworkselect.html', context)


def Homeworklist(request):
    rel = AssignmentQuestionRel.objects.select_related('assignment','solve')

    context = {
        'rel':rel
    }
    return render(request, 'student/Homeworklist.html', context)


def Homeworkcheck(request):
    data = AssignmentQuestionRel.objects.select_related('assignment','question','solve')

    context = {
        'data' : data
    }
    return render(request, 'student/Homeworkcheck.html', context)


def Homeworkcode(request):
    context = {
    }
    return render(request, 'student/Homeworkcode.html', context)


def Notice(request):
    context = {
    }
    return render(request, 'student/Notice.html', context)


def search(request):
    user_input = request.GET['user_input']
    key_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input)

    search_data = []
    for i in key_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question.question_id
        search_data_dict['question_name'] = i.question.question_name
        search_data_dict['question_image'] = i.question.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def search_name(request):
    name_input = request.GET['name_input']
    name_data = Question.objects.filter(question_name__icontains=name_input)

    search_data = []
    for j in name_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = j.question_id
        search_data_dict['question_name'] = j.question_name
        search_data_dict['question_image'] = j.image
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def change_category(request):
    c1 = request.GET['cat_school']
    c2= request.GET['cat_sex']

    context = {
        'c1':c1,
        'c2':c2
    }
    return JsonResponse(context)


def check_code(request):
    code_num = request.GET['code_num']
    # ID_num = request.GET['ID_num']
    try:
        code = Assignment.objects.get(assignment_id=code_num)
    except:
        code=None
    # try:
    #     ID = Solve.objects.get(student_id=ID_num)
    # except:
    #     ID=None or (ID is None)

    if (code is None):
        overlap="fail"
    else:
        overlap="pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)


def check_ID(request):
    ID_num = request.GET['ID_num']

    try:
        ID = Solve.objects.get(student_id=ID_num)
    except:
        ID=None

    if ID is None:
        overlap="fail"
    else:
        overlap="pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)
