from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from school.models import Class, Student, Subject, ClassTeacher, Semester


class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = "school/classes/class_list.html"
    context_object_name = "classes"

    def dispatch(self, request, *args, **kwargs):
        current_date = now().date()
        self.semester = Semester.objects.filter(
            start_date__lte=current_date, end_date__gte=current_date
        ).first()

        if self.semester:
            request.session["semester_id"] = self.semester.id
        else:
            request.session["semester_id"] = None

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        semester_id = self.request.session.get("semester_id")

        if not semester_id:
            return Class.objects.none()

        classes = Class.objects.filter(
            classteacher__teacher=self.request.user,
            classteacher__semester__id=semester_id,
        )

        for cls in classes:
            subject = Subject.objects.filter(
                classteacher__classroom=cls,
                classteacher__teacher=self.request.user,
                classteacher__semester__id=semester_id,
            ).get()
            cls.subject_name = subject.name

            students = Student.objects.filter(
                classstudent__classroom=cls,
                classstudent__semester__id=semester_id,
            )
            cls.student_count = students.count()

            class_teacher = ClassTeacher.objects.filter(
                classroom=cls,
                teacher=self.request.user,
                semester__id=semester_id,
            ).get()
            cls.is_homeroom = class_teacher.is_homeroom

            cls.semester_id = self.semester.id
            cls.semester_name = self.semester.name

        return classes


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "school/students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        semester_id = self.kwargs.get("semester_id")

        return Student.objects.filter(
            classstudent__classroom__id=class_id, classstudent__semester__id=semester_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_id"] = self.kwargs.get("class_id")
        context["semester_id"] = self.kwargs.get("semester_id")
        return context
