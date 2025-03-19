from django.contrib import admin
from .models import Student, Teacher, Class, ClassStudent, ClassTeacher
from .models import (
    Student,
    Class,
    Semester,
    ClassStudent,
    Classification,
    Subject,
    Teacher,
    ClassTeacher,
    Grade,
)

# Register your models here.
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Semester)
admin.site.register(ClassStudent)
admin.site.register(Classification)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(ClassTeacher)
admin.site.register(Grade)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'role')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'semester', 'student', 'late_time', 'absent_time', 'excused_time')
    list_filter = ('classroom', 'semester')


@admin.register(ClassTeacher)
class ClassTeacherAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'semester', 'teacher', 'is_homeroom', 'can_manage')
    list_filter = ('classroom', 'semester', 'is_homeroom', 'can_manage')
