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
    if request.method=="GET":
        return render(request, 'student/Study.html')
    elif request.method=="POST":
        code_num = request.POST.get('code_num')
        ID_num = request.POST.get('ID_num')

        res_data=[]
        if not (code_num and ID_num):
            res_data['error']="코드와 아이디 모두 입력하세요."
        else:
            fuser = AssignmentQuestionRel.objects.get(assignment_id=code_num)

            if che_code(code_num,fuser.assignment_id):
                request.session['user'] = fuser.assignment_id
                return redirect('/')
            else:
                res_data['error']="존재하지 않는 코드입니다."
        return render(request, 'student/Study.html',res_data)

    # context = {
    #
    # }
    # return render(request, 'student/Study.html', context)


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
    question_name = request.GET['question']
    data = Question.objects.filter(question_name=question_name)[0]

    context = {
        'data': data
    }
    return render(request, 'student/AIques.html', context)


def Studyques(request):
    assignment_id = request.GET['code_num']
    data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)[0]

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
    question_id = request.GET['question']

    ques_ans = request.GET['ques_ans']
    school = "/static/student/school_gender_img/" + request.GET['category_school'] +".png"
    gender = "/static/student/school_gender_img/" + request.GET['category_gender'] +".png"

    data = AssignmentQuestionRel.objects.select_related('question','solve').filter(question_id=question_id)[0]

    context = {
        'data': data,
        'ques_ans' : ques_ans,
        'school' : school,
        'gender' : gender,
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
    category_option = request.GET['option']
    opt_data = Question.objects.select_related('category').filter(category__category_name=category_option)

    option_data = []
    for i in opt_data:
        option_data_dict = dict()
        option_data_dict['question_id'] = i.question_id
        option_data_dict['question_name'] = i.question_name
        option_data_dict['question_image'] = i.image
        option_data.append(option_data_dict)

    context = {
        'option_data': option_data
    }
    return JsonResponse(context)


def check_code(request):
    code_num = request.GET['code_num']
    # ID_num = int(request.GET['ID_num'])
    try:
        code = Assignment.objects.get(assignment_id=code_num)
    except:
        code=None
    # try:
    #     ID = Solve.objects.filter(student_id=ID_num)
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
    ID_num = int(request.GET['ID_num'])

    try:
        ID = Solve.objects.filter(student_id=ID_num)
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
