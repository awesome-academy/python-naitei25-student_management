from django.contrib import admin

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
    Attendance,
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
admin.site.register(Attendance)
