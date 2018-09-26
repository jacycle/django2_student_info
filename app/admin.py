from django.contrib import admin
from .models import *
from django.db.models import Avg, Max, Min, Sum
from django.http import HttpResponse
from django.shortcuts import render

# Register your models here.
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'age', 'address',)
    search_fields = ('name', 'subjects__name', )
    list_filter = ('sex',)

class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name',)

class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'score',)

class TeachersAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ScoreListFilter(admin.SimpleListFilter):
    title = '分数段'
    parameter_name = 'scores'

    def lookups(self, request, model_admin):
        return (
            ('0', '小于60'),
            ('1', '大于60'),
            ('2', '最高分'),
            ('3', '最低分'),
            ('4', '总分最高'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(score__lt='60')
        if self.value() == '1':
            return queryset.filter(score__gte='60')
        if self.value() == '2':
            max = queryset.aggregate(Max('score'))
            return queryset.filter(score__gte=max.get('score__max'))
        if self.value() == '3':
            min = queryset.aggregate(Min('score'))
            return queryset.filter(score__lte=min.get('score__min'))
        if self.value() == '4':
            max = 0
            listname = []
            for q in queryset:
                listname.append(q.student.name)
            listname=list(set(listname))
            stuname = listname[0]
            for name in listname:
                tmp = queryset.filter(student__name=name).aggregate(Sum('score')).get('score__sum')
                if (tmp >= max):
                    max = tmp
                    stuname = name
                    print(max)

            return queryset.filter(student__name=stuname)


class StuCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'score', )
    list_filter = ('course__name', ScoreListFilter,)
    actions = ['make_ave_score', 'make_max_score']
    search_fields = ('student__name', )
    ordering = ('course__name','student__name',)
    def make_ave_score(self, request, queryset):
        #ave = StuCourse.objects.all().aggregate(Avg('score'))
        ave = queryset.aggregate(Avg('score'))
        print(ave)
        #return HttpResponse("ave=%s" %(ave.get('score__avg')))
        return render(request, 'ave.html', {'data': ave.get('score__avg')})

    def make_max_score(self, request, queryset):
        max = queryset.aggregate(Max('score'))
        print(max)
        #return HttpResponse("max=%s" %(max.get('score__max')))

admin.site.register(Students, StudentsAdmin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(Teachers, TeachersAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(StuCourse, StuCourseAdmin)
