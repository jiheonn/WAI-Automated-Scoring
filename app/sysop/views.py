from django.shortcuts import render, redirect

# Create your views here.
from mainpage.models import Teacher, MakeQuestion, Question, Category, Mark, AssignmentQuestionRel, Keyword, \
    StudySolveData, Solve, Notice

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

APPROVED_ALLOW = 1
APPROVED_DENY = 0


# 관리자 홈 페이지
def home(request):
    context = {}

    return render(request, "sysop/home.html", context)


# 신규교사정보 페이지
def view_teacher_data(request):
    all_teacher = Teacher.objects.all()
    context = {"teacher": all_teacher}

    return render(request, "sysop/view_teacher_data.html", context)


# 문항검토 페이지
def view_quiz(request):
    all_makequestion = MakeQuestion.objects.all()
    context = {"makequestion": all_makequestion}

    return render(request, "sysop/view_quiz.html", context)


# 문항검토 자세히보기 페이지
def detail_quiz(request):
    question_id = request.GET["question_id"]
    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=question_id
    ).first()
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}

    return render(request, "sysop/detail_quiz.html", context)


# 문항검토 신규문항 생성 페이지
def make_quiz(request):
    context = {}

    return render(request, "sysop/make_quiz.html", context)


# 문항생성 페이지
def view_question(request):
    all_question = Question.objects.all()
    context = {"question": all_question}

    return render(request, "sysop/view_question.html", context)


# 문항생성 자세히보기 페이지
def detail_question(request):
    question_id = request.GET["question_id"]
    question = Question.objects.filter(question_id=question_id).first()
    all_category = Category.objects.all()
    keyword_list=Keyword.objects.filter(question=question_id).values_list('keyword_name', flat=True)
    keyword = ", ".join([i for i in keyword_list])

    context = {"question": question,
               "category": all_category,
               "keyword": keyword}

    return render(request, "sysop/detail_question.html", context)


# 문항검토 신규문항 생성 페이지
def make_question(request):
    all_category = Category.objects.all()

    context = {"category": all_category}

    return render(request, "sysop/make_question.html", context)


# 공지사항 페이지
def view_notice(request):
    all_notice = Notice.objects.all()

    context = {"notice": all_notice}

    return render(request, "sysop/view_notice.html", context)


# 공지사항 자세히보기 페이지
def detail_notice(request):
    notice_id = request.GET["notice_id"]
    notice = Notice.objects.filter(notice_id=notice_id).first()
    notice_target_list = ["공통", "학생", "선생님", "관리자"]
    context = {"notice": notice,
               "notice_target_list": notice_target_list}

    return render(request, "sysop/detail_notice.html", context)


# 공지사항 생성 페이지
def make_notice(request):
    context = {}

    return render(request, "sysop/make_notice.html", context)


# 로그인 함수
@method_decorator(csrf_exempt)
def sysop_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return render(request, "sysop/home.html")
            else:
                messages.error(request, "선생님은 관리자페이지에 접속하실 수 없습니다.")
                return render(request, "sysop/sysop_login.html")
        else:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "sysop/sysop_login.html")

    return render(request, "sysop/sysop_login.html")


# 로그아웃 함수
def sysop_logout(request):
    logout(request)

    return redirect("sysop_login")


# 선생님 승인 함수
def deny_to_allow_teacher_approve(request):
    teacher_id = request.GET.get("teacher_id")
    teacher_info = Teacher.objects.get(teacher_id=teacher_id)
    teacher_info.approve = APPROVED_ALLOW
    teacher_info.save()
    teacher = Teacher.objects.all()

    context = {"teacher": teacher}

    return render(request, "sysop/view_teacher_data.html", context)


# 선생님 승인취소 함수
def allow_to_deny_teacher_approve(request):
    teacher_id = request.GET.get("teacher_id")
    teacher_info = Teacher.objects.get(teacher_id=teacher_id)
    teacher_info.approve = APPROVED_DENY
    teacher_info.save()
    teacher = Teacher.objects.all()

    context = {"teacher": teacher}

    return render(request, "sysop/view_teacher_data.html", context)


# 문항검토 등록 함수
def deny_to_allow_quiz(request):
    make_question_id = request.GET.get("make_question_id")
    make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
    make_question_info.upload_check = APPROVED_ALLOW
    make_question_info.save()
    all_make_question = MakeQuestion.objects.all()

    context = {"makequestion": all_make_question}

    return render(request, "sysop/view_quiz.html", context)


# 문항검토 등록취소 함수
def allow_to_deny_quiz(request):
    make_question_id = request.GET.get("make_question_id")
    make_question_info = MakeQuestion.objects.get(make_question_id=make_question_id)
    make_question_info.upload_check = APPROVED_DENY
    make_question_info.save()
    all_make_question = MakeQuestion.objects.all()

    context = {"makequestion": all_make_question}

    return render(request, "sysop/view_quiz.html", context)


# 문항생성 등록 함수
def deny_to_allow_question(request):
    question_id = request.GET.get("question_id")
    question_info = Question.objects.get(question_id=question_id)
    question_info.upload_check = APPROVED_ALLOW
    question_info.save()
    all_question = Question.objects.all()

    context = {"question": all_question}

    return render(request, "sysop/view_question.html", context)


# 문항생성 등록취소 함수
def allow_to_deny_question(request):
    question_id = request.GET.get("question_id")
    question_info = Question.objects.get(question_id=question_id)
    question_info.upload_check = APPROVED_DENY
    question_info.save()
    all_question = Question.objects.all()

    context = {"question": all_question}

    return render(request, "sysop/view_question.html", context)


# 문항검토 신규문항 생성 함수
def create_quiz(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        TEACHER_ADMIN = 0

        id_number = MakeQuestion.objects.all().last().make_question_id + 1
        image = request.FILES["image"]
        image.name = str(id_number) + "_" + image.name

        make_question_data = MakeQuestion(
            teacher=Teacher.objects.get(teacher_id=TEACHER_ADMIN),
            question_name=request.POST["question_name"],
            description=request.POST["description"],
            answer=request.POST["answer"],
            image=image,
            hint=request.POST["hint"],
            made_date=now_date,
            upload_check=APPROVED_DENY,
        )

        make_question_data.save()
        mark_list = request.POST.getlist("mark_text")

        # MakeQuestion Table 과 연결된 Mark Table 데이터 추가
        for mark_text in mark_list:
            mark_change_data = Mark(mark_text=mark_text, make_question_id=make_question_data.make_question_id)
            mark_change_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("sysop_make_quiz")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("sysop_make_quiz")


# 문항생성시 keyword db 생성 함수
def create_search_keyword_to_db(question_id, search_keyword):
    keyword_list = search_keyword.split(',')
    for keyword in keyword_list:
        keyword_data = Keyword(
            question=Question.objects.filter(question_id=question_id).first(),
            keyword_name=keyword.strip()
        )
        keyword_data.save()

# 문항생성 신규문항 생성 함수
def create_question(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        id_number = Question.objects.all().last().question_id + 1
        image = request.FILES["image"]
        image.name = str(id_number) + "_" + image.name

        question_data = Question(
            category=Category.objects.filter(category_id=request.POST["question_category_id"]).first(),
            question_name=request.POST["question_name"],
            description=request.POST["question_description"],
            answer=request.POST["question_answer"],
            image=image,
            hint=request.POST["question_hint"],
            made_date=now_date,
            ques_concept=request.POST["question_concept"],
            scoring_keyword=request.POST["question_scoring_keyword"].strip(),
            ml_model_check=request.POST["question_ml_model_check"],
            upload_check=APPROVED_DENY,
        )
        question_data.save()
        create_search_keyword_to_db(id_number, request.POST["question_search_keyword"].strip())

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("sysop_make_question")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("sysop_make_question")


# 공지사항 생성 함수
def create_notice(request):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    try:
        notice_data = Notice(
            notice_target=request.POST["notice_target"],
            notice_name=request.POST["notice_name"],
            notice_content=request.POST["notice_content"],
            made_date=now_date
        )
        notice_data.save()

        messages.success(request, "성공적으로 등록되었습니다.")

        return redirect("sysop_make_notice")

    except:
        messages.error(request, "등록에 실패하였습니다. 다시 한번 확인해 주세요.")

        return redirect("sysop_make_notice")


# 문항검토 수정 함수
def change_quiz_info(request):
    self_question_id = request.POST["self_question_id"]

    self_question_info = MakeQuestion.objects.get(make_question_id=self_question_id)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    # 이미지가 없는 경우 패스
    # 이미지가 있는 경우 새로 저장
    image = request.FILES.get('image', False)
    if bool(image) == True:
        image.name = self_question_id + "_" + now_date + "_" + image.name
        self_question_info.image = image

    self_question_info.question_name = request.POST["self_question_name"]
    self_question_info.description = request.POST["self_question_description"]
    self_question_info.answer = request.POST["self_question_answer"]
    self_question_info.hint = request.POST["self_question_hint"]
    self_question_info.save()

    mark_text_list = request.POST.getlist("self_question_mark")
    mark_data_list = Mark.objects.select_related("make_question").filter(
        make_question_id=self_question_id
    )

    for mark_text, mark_data in zip(mark_text_list, mark_data_list):
        mark_change_data = Mark.objects.get(mark_id=mark_data.mark_id)
        mark_change_data.mark_text = mark_text
        mark_change_data.save()

    makequestion = MakeQuestion.objects.select_related("teacher").filter(
        make_question_id=self_question_id
    ).first()
    mark_list = Mark.objects.select_related("make_question").filter(
        make_question_id=self_question_id
    )
    context = {"makequestion": makequestion, "mark_list": mark_list}

    return render(request, "sysop/detail_quiz.html", context)


# 문항수정시 keyword db 수정 함수
def change_search_keyword_to_db(question_id, search_keyword):
    Keyword.objects.filter(question=question_id).delete()
    keyword_list = search_keyword.split(',')
    for keyword in keyword_list:
        keyword_data = Keyword(
            question=Question.objects.filter(question_id=question_id).first(),
            keyword_name=keyword.strip()
        )
        keyword_data.save()


# 문항생성 정보 수정 함수
def change_question_info(request):
    question_id = request.POST["question_id"]

    question_info = Question.objects.get(question_id=question_id)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    # 이미지가 없는 경우 패스
    # 이미지가 있는 경우 새로 저장
    image = request.FILES.get('image', False)
    if bool(image) == True:
        image.name = question_id + "_" + now_date + "_" + image.name
        question_info.image = image

    question_info.question_name = request.POST["question_name"]
    question_info.category = Category.objects.filter(category_id=request.POST["question_category_id"]).first()
    question_info.ml_model_check = request.POST["question_ml_model_check"]
    question_info.scoring_keyword = request.POST["question_scoring_keyword"].strip()
    question_info.ques_concept = request.POST["question_concept"]
    question_info.description = request.POST["question_description"]
    question_info.answer = request.POST["question_answer"]
    question_info.hint = request.POST["question_hint"]

    question_info.save()
    change_search_keyword_to_db(question_id, request.POST["question_search_keyword"].strip())

    question = Question.objects.filter(question_id=question_id).first()
    all_category = Category.objects.all()
    keyword_list=Keyword.objects.filter(question=question_id).values_list('keyword_name', flat=True)
    keyword = ", ".join([i for i in keyword_list])

    context = {"question": question,
               "category": all_category,
               "keyword": keyword}

    return render(request, "sysop/detail_question.html", context)


# 공지사항 정보 수정 함수
def change_notice_info(request):
    notice_id = request.POST["notice_id"]

    notice_info = Notice.objects.get(notice_id=notice_id)

    notice_info.notice_target = request.POST["notice_target"]
    notice_info.notice_name = request.POST["notice_name"]
    notice_info.notice_content = request.POST["notice_content"]
    notice_info.save()

    notice = Notice.objects.filter(notice_id=notice_id).first()
    notice_target_list = ["공통", "학생", "선생님", "관리자"]

    context = {"notice": notice,
               "notice_target_list": notice_target_list}

    return render(request, "sysop/detail_notice.html", context)


# 공지사항 정보 삭제 함수
def delete_notice(request):
    notice_id = request.GET.get("notice_id")
    notice_info = Notice.objects.get(notice_id=notice_id)
    notice_info.delete()

    all_notice = Notice.objects.all()
    context = {"notice": all_notice}

    return render(request, "sysop/view_notice.html", context)
