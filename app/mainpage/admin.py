# admin.py
from django.contrib import admin
from .models import *
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class MarkAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Mark._meta.get_fields()]
    list_display = ['mark_id', 'get_make_question', 'mark_text']
    def get_make_question(self, obj):
        return obj.make_question.question_name
    ordering = ['mark_id']
    get_make_question.short_description = 'question Name'
    search_fields = ['make_question__question_name']
admin.site.register(Mark, MarkAdmin)

class SelfSolveDataAdmin(admin.ModelAdmin):
    list_display = ['self_id', 'get_make_question', 'response', 'score', 'submit_date']
    def get_make_question(self, obj):
        return obj.make_question.question_name
    ordering = ['self_id']
    get_make_question.short_description = 'question Name'
    list_filter = ('score',)
    search_fields = ['make_question__question_name']
admin.site.register(SelfSolveData, SelfSolveDataAdmin)

class MakeQuestionAdmin(admin.ModelAdmin):
    list_display = ['make_question_id', 'get_teacher_name', 'question_name','made_date', 'upload_check']
    def get_teacher_name(self, obj):
        return obj.teacher.teacher_name
    ordering = ['make_question_id']
    get_teacher_name.short_description = 'teacher name'

    list_filter = ('upload_check',)
    search_fields = ['teacher__teacher_name', 'question_name']
admin.site.register(MakeQuestion, MakeQuestionAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'teacher_name', 'school', 'email',
                    'password', 'approve']
    ordering = ['teacher_id']
    list_filter = ('approve',)
    search_fields = ['teacher_name', 'school']
admin.site.register(Teacher, TeacherAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assignment_id', 'get_teacher_name', 'assignment_title', 'type',
                    'start_date', 'end_date', 'made_date', 'grade', 'school_class']
    def get_teacher_name(self, obj):
        return obj.teacher.teacher_name
    ordering = ['made_date']
    get_teacher_name.short_description = 'teacher name'
    list_filter = ('type',
                   ('made_date', DateRangeFilter)
                   )
    search_fields = ['assignment_title', 'teacher']
admin.site.register(Assignment, AssignmentAdmin)

class StudySolveDataAdmin(admin.ModelAdmin):
    list_display = ['study_id', 'get_question_name', 'school', 'gender',
                    'response', 'score', 'submit_date']
    def get_question_name(self, obj):
        return obj.question.question_name
    ordering = ['study_id']
    get_question_name.short_description = 'question_name'
    list_filter = ('score', 'school', 'gender',
                   ('submit_date', DateRangeFilter),
                   )
admin.site.register(StudySolveData, StudySolveDataAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']
    ordering = ['category_id']
admin.site.register(Category, CategoryAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id','get_category_name', 'model_id', 'question_name',
                    'made_date', 'ques_concept']
    def get_category_name(self, obj):
        return obj.category.category_name
    ordering = ['question_id']
    get_category_name.short_description = 'category_name'
    list_filter = ('category__category_name',
                   ('made_date', DateRangeFilter),
                   )
admin.site.register(Question, QuestionAdmin)

class KeywordAdmin(admin.ModelAdmin):
    list_display = ['keyword_id', 'get_question_name','keyword_name']
    def get_question_name(self, obj):
        return obj.question.question_name
    ordering = ['keyword_id']
    get_question_name.short_description = 'question_name'
admin.site.register(Keyword, KeywordAdmin)


class SolveAdmin(admin.ModelAdmin):
    list_display = ['solve_id', 'student_name', 'get_assignment_name', 'get_question_name',
                    'student_id', 'submit_date', 'response','score']
    def get_assignment_name(self, obj):
        return obj.as_qurel.assignment.assignment_title
    def get_question_name(self, obj):
        return obj.as_qurel.question.question_name
    ordering = ['solve_id']
    get_assignment_name.short_description = 'assignment_name'
    get_question_name.short_description = 'question_name'
    list_filter = (
                   ('submit_date', DateRangeFilter),
                   )
    search_fields = ['student_name', 'as_qurel__assignment__assignment_title',
                     'as_qurel__question__question_name', 'student_id']
admin.site.register(Solve, SolveAdmin)

class AssignmentQuestionRelAdmin(admin.ModelAdmin):
    list_display = ['as_qurel_id', 'get_assignment_id', 'get_assignment_name', 'get_question_name']
    def get_assignment_id(self, obj):
        return obj.assignment.assignment_id
    def get_assignment_name(self, obj):
        return obj.assignment.assignment_title
    def get_question_name(self, obj):
        return obj.question.question_name
    ordering = ['as_qurel_id']
    get_assignment_id.short_description = 'assignment_id'
    get_assignment_name.short_description = 'assignment_name'
    get_question_name.short_description = 'question_name'
    search_fields = ['assignment__assignment_id', 'assignment__assignment_title',
                     'question__question_name']
admin.site.register(AssignmentQuestionRel, AssignmentQuestionRelAdmin)