from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mainpage.models import *
from .models import User
from django.http import JsonResponse
from django.db.models import Q, Max

import datetime
import string
import random
import json

# Create your views here.
# from django.http import HttpResponse, HttpResponseRedirect


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


# 문항선택 화면 view 함수
def question_selection(request):
    question_queryset = Question.objects.filter(upload_check=True)
    category_queryset = Category.objects.all()

    context = {"question_data": question_queryset, "category_data": category_queryset}
    return render(request, "teacher/question_selection.html", context)


# 날짜 형식에 맞게 생성
def created_date(date):
    result = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return result


# 문항선택 > 문항선택완료 버튼 클릭 시  Assignment Table DB 저장
def question_selection_save(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        teacher_id = int(request.POST["teacher_id"])
        selected_question_list = request.POST.getlist("question")
        assignment_data = Assignment(
            assignment_id=request.POST["code_num"],
            teacher=Teacher.objects.get(teacher_id=teacher_id),
            assignment_title=request.POST["question-title"],
            type=request.POST["evaluation_type"],
            start_date=created_date(request.POST["start-date"]),
            end_date=created_date(request.POST["end-date"]),
            made_date=now_date,
            grade=int(request.POST["grade"]),
            school_class=int(request.POST["class"]),
        )
        assignment_data.save()

        # Assignment Table 과 연결된 AssignmentQuestionRel Table 에 데이터 추가
        for question_id in selected_question_list:
            assignment_question_rel_data = AssignmentQuestionRel(
                question_id=int(question_id), assignment_id=request.POST["code_num"]
            )

            assignment_question_rel_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

    return redirect("teacher_question_selection")


# 결과보기 화면 view 함수
def view_result(request):
    # teacher_id = 1
    teacher_id = request.POST["teacher_id"]
    asi_data = Assignment.objects.filter(teacher_id=teacher_id).order_by("start_date")

    context = {"assignment_data": asi_data}
    return render(request, "teacher/view_result.html", context)


# 결과보기 > 더보기 클릭 시 보여지는 화면 view 함수
def view_result_detail(request):
    request_selection_code = request.GET["select_code"]  # 사용자가 요청한 코드
    assignment_queryset = Assignment.objects.all().filter(
        assignment_id=request_selection_code
    )
    assignment_type = ""
    for assignment_information in assignment_queryset:
        assignment_type = assignment_information.type

    solve_queryset = (
        Solve.objects.select_related("as_qurel")
        .filter(
            Q(as_qurel_id__assignment_id=request_selection_code)
            & Q(as_qurel__question__upload_check=True)
        )
        .order_by("student_id")
    )  # 요청된 코드에 속하는 solve queryset
    count_question = (
        solve_queryset.values("as_qurel_id__question_id").distinct().count()
    )  # 중복 제외 문항 수

    # 한 학생은 여러 score 와 response 를 가집니다.
    # 따라서 하나의 student_id(=result key 값)에 여러 해당하는 데이터의 삽입이 필요합니다. (중복 해결)
    # ex) {12345678: {'student_name': '가나다', 'student_response': ['~~~', '~~~', '~~~']}}
    result = {}
    for solve_information in solve_queryset:
        solve_question_data = {}
        if solve_information.student_id in result:
            result[solve_information.student_id][
                "student_id"
            ] = solve_information.student_id
            result[solve_information.student_id]["student_score"].append(
                int(solve_information.score)
            )
            result[solve_information.student_id]["student_response"].append(
                solve_information.response
            )
        else:
            solve_question_data["student_progress"] = []
            solve_question_data["student_score"] = []
            solve_question_data["student_response"] = []
            solve_question_data["student_id"] = solve_information.student_id
            solve_question_data["student_name"] = solve_information.student_name
            solve_question_data["student_score"].append(int(solve_information.score))
            solve_question_data["student_response"].append(solve_information.response)

            result[solve_information.student_id] = solve_question_data

    for student_id in result:  # 한 학생의 평균 점수 구하기
        student_data = result[student_id]
        result[student_id]["student_score"] = sum(student_data["student_score"]) / len(
            student_data["student_score"]
        )

    total_score = 0  # 총 점수
    total_progress = 0  # 총 진행률
    all_avg = 0  # 전체 학생 평균 점수
    all_progress = 0  # 전체 학생 평균 진행률
    for j in result.values():
        total_score += j["student_score"]
        if len(j["student_response"]) >= 1:
            count = len(j["student_response"])
            j["student_progress"] = round(count / count_question * 100)
        total_progress += j["student_progress"]
    
    number_of_students = len(result.values())
    if number_of_students != 0:
        all_avg = round(total_score / len(result.values()), 2)  # 전체 학생 평균 점수
        all_progress = round(total_progress / len(result.values()))  # 전체 학생 평균 진행률
    else:
        all_avg = 0
        all_progress = 0

    context = {
        "assignment_data": assignment_queryset,
        "assignment_type": assignment_type,
        "question_count": count_question,
        "result": result.values(),
        "result_item": result.items(),
        "all_avg": all_avg,
        "all_pgs": all_progress,
    }
    return render(request, "teacher/view_result_detail.html", context)


# 문항생성 화면 view 함수
def make_question(request):
    return render(request, "teacher/make_question.html")


# 문항생성 > 문항생성완료 버튼 클릭 시  MakeQuestion Table DB 저장
def make_question_save(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    id_number = MakeQuestion.objects.all().last().make_question_id + 1
    image = request.FILES["image"]
    image.name = str(id_number) + "_" + image.name

    try:
        teacher_id = int(request.POST["teacher_id"])
        make_question_data = MakeQuestion(
            teacher=Teacher.objects.get(teacher_id=teacher_id),
            question_name=request.POST["question_name"],
            description=request.POST["description"],
            answer=request.POST["answer"],
            image=image,
            hint=request.POST["hint"],
            made_date=now_date,
            upload_check=0,
        )
        make_question_data.save()

        mark_list = request.POST.getlist("mark_text")
        temp = MakeQuestion.objects.get(hint=request.POST["hint"], made_date=now_date)
        # MakeQuestion Table 과 연결된 Mark Table 데이터 추가
        for i in mark_list:
            mark_data = Mark(mark_text=i, make_question_id=temp.make_question_id)
            mark_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

    return redirect("teacher_make_question")


# Bigram Tree 화면 view 함수
def bigram_tree(request):
    return render(request, "teacher/bigram_tree.html")


# 주제분석 화면 view 함수
def topic_analysis(request):
    return render(request, "teacher/topic_analysis.html")


# 응답분석 화면 view 함수
def response_analysis(request):
    return render(request, "teacher/response_analysis.html")


# QR 코드 화면 view 함수
def qr_code(request):
    question_data = Question.objects.all()
    context = {"question_data": question_data}
    return render(request, "teacher/QR_code.html", context)


# 공지사항 화면 view 함수
def teacher_notice(request):
    all_notice = Notice.objects.exclude(notice_target="학생")
    context = {"notice": all_notice}
    return render(request, "teacher/teacher_notice.html", context)


# 공지사항 자세히보기 화면 view 함수
def teacher_notice_detail(request):
    notice_id = request.GET["selected_notice_id"]
    notice = Notice.objects.filter(notice_id=notice_id).first()
    context = {"notice": notice}
    return render(request, "teacher/teacher_notice_detail.html", context)


# 문항선택 > 문항 검색 함수
def question_search(request):
    user_input = request.GET["user_input"]
    seach_data = (
        Keyword.objects.select_related("question")
        .filter(
            (
                Q(keyword_name__icontains=user_input)
                | Q(question__question_name__icontains=user_input)
            )
            & Q(question__upload_check=True)
        )
        .values_list("question_id", flat=True)
        .distinct()
    )
    data = Question.objects.filter(pk__in=seach_data)

    search_data = []
    for i in data:
        search_data_dict = dict()
        search_data_dict["question_id"] = i.question_id
        search_data_dict["question_name"] = i.question_name
        search_data_dict["question_image"] = json.dumps(str(i.image)).replace('"', "")
        search_data.append(search_data_dict)

    context = {"search_data": search_data}
    return JsonResponse(context)


# 문항선택 > 기존 시험지 복사 버튼 클릭 시 작동 함수
def assignment_copy(request):
    copy_code = request.GET["copy_code"]
    cp_data = AssignmentQuestionRel.objects.select_related(
        "assignment", "question"
    ).filter(assignment_id=copy_code)

    copy_data = []
    for i in cp_data:
        copy_data_dict = dict()
        copy_data_dict["question_id"] = i.question.question_id
        copy_data_dict["assignment_type"] = i.assignment.type
        copy_data_dict["assignment_title"] = i.assignment.assignment_title
        copy_data.append(copy_data_dict)

    context = {"copy_data": copy_data}
    return JsonResponse(context)


# 문항선택 > 카테고리 변경 시 작동 함수
def change_category(request):
    category_option = request.GET["option"]
    if category_option == "select":
        opt_data = Question.objects.all()
    else:
        opt_data = Question.objects.select_related("category").filter(
            category__category_name=category_option
        )

    option_data = []
    for i in opt_data:
        option_data_dict = dict()
        option_data_dict["question_id"] = i.question_id
        option_data_dict["question_name"] = i.question_name
        option_data_dict["question_image"] = json.dumps(str(i.image)).replace('"', "")
        option_data.append(option_data_dict)

    context = {"option_data": option_data}
    return JsonResponse(context)


# 문항선택 > 코드 생성 버튼 클릭시 작동 함수
def code_generation(request):
    generation_code = request.GET["text"]
    assignment_id = Assignment.objects.all().values("assignment_id")

    _LENGTH = 8
    string_pool = string.ascii_uppercase + string.digits

    for i in assignment_id:
        if i == generation_code:
            result = ""
            for j in range(_LENGTH):
                result += random.choice(string_pool)
        else:
            generation_code = generation_code

    context = {"generation_code": generation_code}
    return JsonResponse(context)


# 홈 > 로그인 함수
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            queryset = Teacher.objects.filter(email=username)
            for teacher_information in queryset:
                is_approve = teacher_information.approve
                if is_approve:
                    login(request, user)
                else:
                    messages.error(request, "관리자의 승인이 필요합니다.")
        else:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")

    return render(request, "teacher/login.html")


# 로그아웃 함수
def logout_view(request):
    logout(request)
    return redirect("teacher_login")


# 회원가입 함수
def signup_view(request):
    latested_teacher_id = Teacher.objects.aggregate(teacher_id=Max("teacher_id"))
    teacher_id = latested_teacher_id["teacher_id"] + 1
    try:
        if request.method == "POST":
            if request.POST["password1"] == request.POST["password2"]:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.last_name = request.POST["last_name"]
                user.first_name = request.POST["first_name"]
                user.teacher_id = request.POST["teacher_id"]
                user.save()

                teacher_data = Teacher(
                    teacher_name=request.POST["last_name"] + request.POST["first_name"],
                    school=request.POST["school"],
                    email=request.POST["username"],
                    password=request.POST["password1"],
                    approve=False,
                )

                teacher_data.save()

                messages.success(request, "회원가입이 완료되었습니다.")

                return redirect("teacher_login")
    except:
        messages.error(request, "비밀번호가 일치하지 않거나 중복된 이메일입니다.")

        return redirect("teacher_signup")

    return render(request, "teacher/signup.html", {"teacher_id": teacher_id})


# 결과보기 > 더보기 > 더보기 클릭 시 결과를 차트로 보여주는 기능
def chart(request):
    studnet_name = request.POST.getlist("student_name")
    studnet_score = request.POST.getlist("student_score")

    labels = studnet_name
    data = []

    for i in studnet_score:
        data.append(float(i))

    context = {"labels": labels, "data": data}
    return render(request, "teacher/chart.html", context)

