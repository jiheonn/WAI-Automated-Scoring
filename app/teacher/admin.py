from django.contrib import admin
from mainpage.models import *
from .models import User
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


admin.site.register(User)


class AssignmentQuestionRelInline(admin.TabularInline):
    model = AssignmentQuestionRel


class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'assignment_id', 'teacher', 'assignment_title', 'type',
        'start_date', 'end_date', 'made_date', 'grade', 'school_class'
    ]
    list_filter = (
        'type',
        ('made_date', DateRangeFilter)
    )
    search_fields = [
        'assignment_id', 'assignment_title'
    ]
    list_display_links = ['assignment_id']
    inlines = [
        AssignmentQuestionRelInline
    ]


admin.site.register(Assignment, AssignmentAdmin)


# class SolveInline(admin.TabularInline):
#     model = Solve
#
#
# @admin.register(AssignmentQuestionRel)
# class AssignmentQuestionRelAdmin(admin.ModelAdmin):
#     list_display = [
#         'as_qurel_id', 'assignment', 'question'
#     ]
#     inlines = [
#         SolveInline
#     ]


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category_id', 'category_name'
    ]
    list_display_links = ['category_id']
    inlines = [
        QuestionInline
    ]


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = [
        'keyword_id', 'question', 'keyword_name'
    ]
    list_display_links = ['keyword_id']


class MarkInline(admin.TabularInline):
    model = Mark


class MakeQuestionAdmin(admin.ModelAdmin):
    list_display = [
        'make_question_id', 'teacher', 'question_name', 'discription',
        'answer', 'image', 'hint', 'made_date', 'upload_check'
    ]
    list_display_links = ['make_question_id']
    list_filter = (
        'upload_check',
        ('made_date', DateRangeFilter)
    )
    search_fields = [
        'question_name'
    ]
    inlines = [
        MarkInline
    ]


admin.site.register(MakeQuestion, MakeQuestionAdmin)


# @admin.register(Mark)
# class MarkAdmin(admin.ModelAdmin):
#     list_display = [
#         'mark_id', 'make_question', 'mark_text'
#     ]
#     list_display_links = ['mark_id']


class KeywordInline(admin.TabularInline):
    model = Keyword


class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_id', 'category', 'model_id', 'question_name', 'discription',
        'answer', 'image', 'hint', 'made_date', 'qr_code', 'ques_concept'
    ]
    list_display_links = ['question_id']
    list_filter = (
        'category__category_name',
        ('made_date', DateRangeFilter)
    )
    search_fields = [
        'question_name'
    ]
    inlines = [
        KeywordInline, AssignmentQuestionRelInline
    ]


admin.site.register(Question, QuestionAdmin)


@admin.register(Solve)
class SolveAdmin(admin.ModelAdmin):
    list_display = [
        'solve_id', 'as_qurel', 'student_id', 'submit_date',
        'response', 'score', 'student_name'
    ]
    list_display_links = ['student_id']


class AssignmentInline(admin.TabularInline):
    model = Assignment


class MakeQuestionInline(admin.TabularInline):
    model = MakeQuestion


class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'teacher_id', 'teacher_name', 'school',
        'email', 'password', 'approve'
    ]
    list_display_links = ['teacher_name']
    list_filter = (
        'approve',
    )
    search_fields = [
        'teacher_name', 'school'
    ]
    inlines = [
        AssignmentInline, MakeQuestionInline
    ]


admin.site.register(Teacher, TeacherAdmin)

