from django.contrib import admin
from mainpage.models import SelfSolveData, MakeQuestion, StudySolveData, Question
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


# Register your models here.


class SelfSolveDataAdmin(admin.ModelAdmin):
    list_display = [
        'self_id', 'make_question', 'response', 'score', 'submit_date'
    ]
    list_display_links = ['self_id']
    list_filter = ('score', ('submit_date', DateRangeFilter))


admin.site.register(SelfSolveData, SelfSolveDataAdmin)


class StudySolveDataAdmin(admin.ModelAdmin):
    list_display = [
        'study_id', 'question', 'school', 'gender', 'response', 'score', 'submit_date'
    ]
    list_display_links = ['study_id']
    list_filter = ('score', ('submit_date', DateRangeFilter))


admin.site.register(StudySolveData, StudySolveDataAdmin)