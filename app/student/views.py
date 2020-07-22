from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import q as q
from django.db.models import Q
import datetime

from mainpage.models import Question, SelfSolveData, AssignmentQuestionRel, Keyword, Solve, Assignment, MakeQuestion, \
    Category, StudySolveData, Mark


def index(request):
    context = {
    }
    return render(request, 'student/index.html', context)

#TODO : 함수명은 대문자를 쓰지 않습니다. 수정 필요
def AI(request):
    qs = Question.objects.all()
    category = Category.objects.all()

    context = {
        'qs': qs,
        'category': category
    }
    return render(request, 'student/AI.html', context)


#TODO : 함수명은 대문자를 쓰지 않습니다. 수정 필요
def AIques(request):
    question_id = int(request.GET['question_id'])
    data = Question.objects.filter(question_id=question_id)[0]
    context = {
        'data': data
    }
    return render(request, 'student/AIques.html', context)


#TODO : 함수명은 대문자를 쓰지 않습니다. 수정 필요
def AIdiag(request):
    question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    # 학교,성별 이미지 출력
    re_school = request.GET.get('category_school')
    re_gender = request.GET.get('category_gender')

    if (re_school != "") and (re_gender != ""):
        school = f'/staticfiles/student/school_gender_img/{re_school}.png'
        gender = f'/staticfiles/student/school_gender_img/{re_gender}.png'
    else: 
        school = ""
        gender = ""

    # TODO: 불명확한 변수 이름, 더 명확한 변수명을 사용하세요
    key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = key[0] #TODO : 남들이 알아볼 수 있는 쉬운 이름으로 작성하세요

    # TODO: 불명확한 변수 이름, 더 명확한 변수명을 사용하세요
    # solve테이블과 question테이블 조인
    as_qurel_id = key.values('as_qurel_id')[0]['as_qurel_id'] #TODO : 함수화를 시켜주세요
    da = Solve.objects.prefetch_related('assignment_question_rel').filter(as_qurel_id=as_qurel_id)

    context = {
        'data': data,
        'ques_ans': ques_ans,
        'school': school,
        'gender': gender,
    }

    # 나의 답 DB에 저장
    # ssd = StudySolveData.objects.select_related('question').filter(question__question_id=question_id)
    # TODO : 이미 받아온 값을 한 번더 받아오지 마세요
    try:
        study_solve_data = StudySolveData(
            question_id=question_id,
            school=request.GET['category_school'],
            gender=request.GET['category_gender'],
            response=ques_ans,
            score=0, #TODO : 초기값이라면 대문자로 상수를 만들어서 의미를 부여하세요.
            submit_date=now_date
        )
        # TODO :  필요없는 프린트문은 삭제하세요
        print(study_solve_data)
        study_solve_data.save()

    except:
        study_solve_data = None

    return render(request, 'student/AIdiag.html', context)

# TODO : 함수명을 확인하세요
def Study(request):
    context = {
    }
    return render(request, 'student/Study.html', context)

# TODO : 함수명을 확인하세요
def Studyques(request):
    try:
        # study페이지에서 숙제 코드 가져오기
        assignment_id = request.GET['code_num']
        student_id = request.GET['ID_num']
        student_name = request.GET['student_name']

        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id).filter(
            assignment__type="학습평가")
        f = data[0]

        # 코드가 db에 없으면 원상복귀
        if (f == None) or (student_id == "") or (student_name == ""):
            context = {
            }
            return render(request, 'student/Study.html', context)
        # TODO : 쓰지않는 주석문은 제거하세요
        # context = {
        #     'data': data,
        #     'f': f,
        #     'done_list': done_list
        # }
        # return render(request, 'student/Studyques.html', context)

    # TODO : try except 구문을 쓸 때는 다시한번 고려해주세요
    except:
        try:
            # id로 문항 불러오기
            question_info = request.GET['question_id'].split(',')
            question_id = int(question_info[0])
            assignment_id = question_info[1]

            data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
            key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
            f = key[0]

        except:
            pass #TODO : 의미없는 pass는 쓰지마세요
        

    # 문항 학습 완료여부 판단
    test_list = []
    done_list = []
    # TODO: 변수명의 a 또는 b 처럼 의미없는 알파벳을 쓰지마세요
    for a in data:
        as_qurel_id = a.as_qurel_id
        ttt = Solve.objects.filter(as_qurel_id=as_qurel_id)
        test_list.append(ttt)
    for i in test_list:
        if i.values('as_qurel_id'):
            done = "O"
        else:
            done = "X"
        done_list.append(done)

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    # 나의 답 DB에 저장
    try:
        solve_data = Solve(
            student_id=student_id,
            submit_date=now_date,
            response=request.GET['ques_ans'],
            score=0,
            as_querl_id=as_qurel_id,
            student_name=student_name
        )
        solve_data.save()

    except:
        solve_data = None

    context = {
        'data': data,
        'f': f,
        'done_list': done_list
    }
    return render(request, 'student/Studyques.html', context)

    # TODO : 삭제
    # except:
    #     context = {
    #         'data': data,
    #         'f': f
    #     }

    # finally:
    #     print(request.GET['ques_ans'])
    # question_id = f.question_id
    # key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    # as_qurel_id = key.values('as_qurel_id')[0]['as_qurel_id']
    #
    # # 나의 답 DB에 저장
    # try:
    #     solve_data = Solve(
    #         student_id=student_id,
    #         submit_date=now_date,
    #         response=request.GET['ques_ans'],
    #         score=0,
    #         as_querl_id=as_qurel_id,
    #         student_name=student_name
    #     )
    #     solve_data.save()
    #
    # except:
    #     solve_data = None
    # return render(request, 'student/Studyques.html', context)

# TODO : 함수명 확인
def Homework(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)

# TODO : 함수명 확인
def Homeworkques(request):
    try:
        # Homeworkques페이지에서 숙제 코드 가져오기
        assignment_id = request.GET['code_num']
        student_id = request.GET['ID_num']
        student_name = request.GET['student_name']

        data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id).filter(
            assignment__type="숙제하기")
        f = data.first()

        # 코드가 db에 없으면 원상복귀
        # TODO : 복잡한 if 문 함수로 변환을 해주세요
        if (f == None) or (student_id == "") or (student_name == ""):
            context = {
            }
            return render(request, 'student/Homeworkcode.html', context)

        # TODO :  의미없는 주석은 삭제
        # context = {
        #     'student_id': student_id,
        #     'data': data,
        #     'f': f,
        #     'student_name': student_name,
        # }
        # return render(request, 'student/Homeworkques.html', context)

    except:
        try:
            # id로 문항 불러오기
            question_info = request.GET['question_id'].split(',')
            question_id = int(question_info[0])
            assignment_id = question_info[1]
            student_id = request.GET['student_id']
            # student_name = request.GET['student_name']

            data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
            f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)[0]

            # context = {
            #     'student_id': student_id,
            #     'data': data,
            #     'f': f
            #     # 'student_name': student_name
            # }
            # return render(request, 'student/Homeworkques.html', context)
        except:
            pass

    # 문항 학습 완료여부 판단
    # TODO : 똑같은 코드를 copy & paste 했다면 코드의 중복을 제거할 수 있도록 고민해주세요
    test_list = []
    done_list = []
    for a in data:
        as_qurel_id = a.as_qurel_id
        ttt = Solve.objects.filter(as_qurel_id=as_qurel_id)
        test_list.append(ttt)
    for i in test_list:
        if i.values('as_qurel_id'):
            done = "O"
        else:
            done = "X"
        done_list.append(done)

    context = {
        'student_id': student_id,
        'data': data,
        'f': f,
        'done_list': done_list,
        'student_name': student_name
    }
    return render(request, 'student/Homeworkques.html', context)

# TODO : 함수명을 확인해주세요 
def Homeworkdiag(request):
    question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']
    student_id = request.GET['student_id']

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    key = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = key[0]

    # solve테이블과 question테이블 조인
    as_qurel_id = key.values('as_qurel_id')[0]['as_qurel_id']
    da = Solve.objects.prefetch_related('assignment_question_rel').filter(as_qurel_id=as_qurel_id)

    context = {
        'student_id': student_id,
        'ques_ans': ques_ans,
        'data': data,
    }
    # return render(request, 'student/Homeworkdiag.html', context)

    # 나의 답 DB에 저장
    try:
        solve_data = Solve(
            student_id=student_id,
            submit_date=now_date,
            response=ques_ans,
            score=0,
            as_querl_id=as_qurel_id,
            student_name=request.GET['student_name']
        )
        solve_data.save()

    except:
        solve_data = None

    return render(request, 'student/Homeworkdiag.html', context)


def Homeworkselect(request):
    context = {
    }
    return render(request, 'student/Homeworkselect.html', context)


def Homeworklist(request):
    # question_info = request.GET['question_name'].split(',')
    # question_name = question_info[0]
    # assignment_id = question_info[1]
    # data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
    # f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]
    student_id = int(request.GET['ID_num'])
    # rel = AssignmentQuestionRel.objects.select_related('assignment', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    rel = AssignmentQuestionRel.objects.prefetch_related('assignment').filter(as_qurel_id=d)

    context = {
        'rel': rel,
        # 'da':da,
        're': re
    }
    return render(request, 'student/Homeworklist.html', context)


def Homeworkcheck(request):
    student_id = int(request.GET['student_id'])
    # assignment_title = request.GET['assignment_id']
    # print(assignment_title.values())
    # data = AssignmentQuestionRel.objects.select_related('assignment', 'question', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    data = AssignmentQuestionRel.objects.prefetch_related('assignment', 'question').filter(as_qurel_id=d)

    context = {
        'data': data
    }
    return render(request, 'student/Homeworkcheck.html', context)


def Homeworkcode(request):
    context = {
    }
    return render(request, 'student/Homeworkcode.html', context)


def Self(request):
    qs = MakeQuestion.objects.all()
    # category = Category.objects.all()

    context = {
        'qs': qs,
        # 'category': category,
    }
    return render(request, 'student/Self.html', context)


def Selfques(request):
    make_question_id = int(request.GET['make_question_id'])
    data = MakeQuestion.objects.filter(make_question_id=make_question_id)[0]

    context = {
        'data': data
    }
    return render(request, 'student/Selfques.html', context)


def self_diagnosis_view(request):
    try:
        make_question_id = int(request.GET['question'])
        ques_ans = request.GET['ques_ans']

        mark = Mark.objects.select_related('make_question').filter(make_question_id=make_question_id)
        data = mark.first()
        print(data)

        context = {
            'data': data,
            'ques_ans': ques_ans,
            'mark': mark
        }
        return render(request, 'student/Selfdiag.html', context)

    except:
        try:
            score_list = request.GET.getlist('score')
            print(score_list + "hi")
        except:
            print("no")
        context = {'score_list': score_list}
        return render(request, 'student/Selfdiag.html', context)


def Selfgrade(request):
    make_question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']
    score_list = request.GET.getlist('score')

    # 점수 합산
    sum_s = 0
    for i in score_list:
        sum_s += int(i)

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    context = {
        'sum_s': sum_s
    }

    # 나의 답 DB에 저장
    try:
        self_solve_data = SelfSolveData(
            make_question_id=make_question_id,
            response=ques_ans,
            score=sum_s,
            submit_date=now_date
        )
        self_solve_data.save()

    except:
        self_solve_data = None

    return render(request, 'student/Selfgrade.html', context)


def Notice(request):
    context = {
    }
    return render(request, 'student/Notice.html', context)


def search(request):
    user_input = request.GET['user_input']
    key_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input).values_list(
        'question_id', flat=True).distinct()
    k_data = Question.objects.filter(pk__in=key_data)

    search_data = []
    for i in k_data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question_id
        search_data_dict['question_name'] = i.question_name
        search_data_dict['question_image'] = i.image.name
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def search_name(request):
    name_input = request.GET['name_input']
    name_data = MakeQuestion.objects.filter(question_name__icontains=name_input).values_list('make_question_id',
                                                                                             flat=True).distinct()
    n_data = MakeQuestion.objects.filter(pk__in=name_data)

    search_data = []
    for j in n_data:
        search_data_dict = dict()
        search_data_dict['make_question_id'] = j.make_question_id
        search_data_dict['question_name'] = j.question_name
        search_data_dict['question_image'] = j.image.name
        search_data.append(search_data_dict)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def change_category_self(request):
    category_option = request.GET['option']

    if category_option == 'select':
        opt_data = Question.objects.all()
    else:
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


def change_category(request):
    category_option = request.GET['option']

    if category_option == 'select':
        opt_data = Question.objects.all()
    else:
        opt_data = Question.objects.select_related('category').filter(category__category_name=category_option)

    option_data = []
    for i in opt_data:
        option_data_dict = dict()
        option_data_dict['question_id'] = i.question_id
        option_data_dict['question_name'] = i.question_name
        option_data_dict['question_image'] = i.image.name
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
        code = None
    # try:
    #     ID = Solve.objects.filter(student_id=ID_num)
    # except:
    #     ID=None or (ID is None)

    if (code is None):
        overlap = "fail"
    else:
        overlap = "pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)


def check_ID(request):
    ID_num = int(request.GET['ID_num'])

    try:
        ID = Solve.objects.filter(student_id=ID_num)
    except:
        ID = None

    if ID is None:
        overlap = "fail"
    else:
        overlap = "pass"

    context = {
        'overlap': overlap
    }
    return JsonResponse(context)
