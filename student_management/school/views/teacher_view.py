from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.db.models import Q
from django.forms import formset_factory

from school.models import (
    Class,
    Student,
    Subject,
    Semester,
    ClassTeacher,
    ClassStudent,
    Attendance,
    Grade,
)
from school.forms import AttendanceForm, GradeForm


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

    def dispatch(self, request, *args, **kwargs):
        if "class_id" in kwargs:
            request.session["class_id"] = kwargs["class_id"]

        if "semester_id" in kwargs:
            request.session["semester_id"] = kwargs["semester_id"]

        subject = Subject.objects.filter(
            classteacher__classroom_id=request.session["class_id"],
            classteacher__semester__id=request.session["semester_id"],
            classteacher__teacher=self.request.user,
        ).first()
        request.session["subject_id"] = subject.id

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        semester_id = self.kwargs.get("semester_id")
        class_teacher = ClassTeacher.objects.filter(
            classroom__id=class_id,
            semester__id=semester_id,
            teacher=self.request.user,
        ).get()
        self.is_homeroom = class_teacher.is_homeroom

        query = self.request.GET.get("student_name", "")

        if query:
            return Student.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query),
                classstudent__classroom__id=class_id,
                classstudent__semester__id=semester_id,
            )

        return Student.objects.filter(
            classstudent__classroom__id=class_id, classstudent__semester__id=semester_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_id"] = self.kwargs.get("class_id")
        context["semester_id"] = self.kwargs.get("semester_id")
        context["subject_id"] = self.request.session.get("subject_id")
        context["is_homeroom"] = self.is_homeroom
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "school/students/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_id"] = self.request.session.get("class_id") or None
        context["semester_id"] = self.request.session.get("semester_id") or None
        context["subject_id"] = self.request.session.get("subject_id") or None
        return context


class AttendancesView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "school/attendances/attendance_tracking.html"
    context_object_name = "attendances"

    def dispatch(self, request, *args, **kwargs):
        if "class_id" in kwargs:
            request.session["class_id"] = kwargs["class_id"]

        if "semester_id" in kwargs:
            request.session["semester_id"] = kwargs["semester_id"]

        subject = Subject.objects.filter(
            classteacher__classroom_id=request.session["class_id"],
            classteacher__semester__id=request.session["semester_id"],
            classteacher__teacher=self.request.user,
        ).first()
        request.session["subject_id"] = subject.id

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        semester_id = self.kwargs.get("semester_id")
        class_teacher = ClassTeacher.objects.filter(
            classroom__id=class_id,
            semester__id=semester_id,
            teacher=self.request.user,
        ).get()
        self.is_homeroom = class_teacher.is_homeroom

        class_students = ClassStudent.objects.filter(
            classroom__id=class_id, semester__id=semester_id
        )

        query = self.request.GET.get("student_name", "")
        if query:
            class_students = class_students.filter(
                Q(student__first_name__icontains=query)
                | Q(student__last_name__icontains=query)
            )

        attendance_ids = []
        for class_student in class_students:
            attendance, created = Attendance.objects.get_or_create(
                classstudent=class_student, date=now().date()
            )
            attendance_ids.append(attendance.id)

        return Attendance.objects.filter(id__in=attendance_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendances = self.get_queryset()

        AttendanceFormSet = formset_factory(AttendanceForm, extra=0)
        formset = AttendanceFormSet(
            initial=[
                {"classstudent_id": a.classstudent.id, "status": a.status}
                for a in attendances
            ]
        )

        form_attendance_pairs = zip(formset.forms, attendances)

        context["current_date"] = now().date()
        context["class_id"] = self.kwargs.get("class_id")
        context["semester_id"] = self.kwargs.get("semester_id")
        context["subject_id"] = self.request.session.get("subject_id")
        context["is_homeroom"] = self.is_homeroom
        context["formset"] = formset
        context["form_attendance_pairs"] = form_attendance_pairs

        return context


class GradeView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = "school/grades/grade_list.html"
    context_object_name = "grades"

    def dispatch(self, request, *args, **kwargs):
        if "class_id" in kwargs:
            request.session["class_id"] = kwargs["class_id"]

        if "semester_id" in kwargs:
            request.session["semester_id"] = kwargs["semester_id"]

        if "subject_id" in kwargs:
            request.session["subject_id"] = kwargs["subject_id"]

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        semester_id = self.kwargs.get("semester_id")
        subject_id = self.kwargs.get("subject_id")
        class_teacher = ClassTeacher.objects.filter(
            classroom__id=class_id,
            semester__id=semester_id,
            teacher=self.request.user,
        ).get()
        self.is_homeroom = class_teacher.is_homeroom

        class_students = ClassStudent.objects.filter(
            classroom__id=class_id, semester__id=semester_id
        )

        query = self.request.GET.get("student_name", "")
        if query:
            class_students = class_students.filter(
                Q(student__first_name__icontains=query)
                | Q(student__last_name__icontains=query)
            )

        grade_ids = []
        for class_student in class_students:
            grade, created = Grade.objects.get_or_create(
                classstudent=class_student, subject__id=subject_id
            )
            grade_ids.append(grade.id)

        return Grade.objects.filter(id__in=grade_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grades = self.get_queryset()

        GradeFormSet = formset_factory(GradeForm, extra=0)
        formset = GradeFormSet(
            initial=[
                {
                    "classstudent_id": a.classstudent.id,
                    "oral_score": a.oral_score,
                    "fifteen_min_score": a.fifteen_min_score,
                    "one_period_score": a.one_period_score,
                    "midterm_score": a.midterm_score,
                    "final_score": a.final_score,
                }
                for a in grades
            ]
        )

        form_grade_pairs = zip(formset.forms, grades)

        context["current_date"] = now().date()
        context["class_id"] = self.kwargs.get("class_id")
        context["semester_id"] = self.kwargs.get("semester_id")
        context["subject_id"] = self.kwargs.get("subject_id")
        context["is_homeroom"] = self.is_homeroom
        context["formset"] = formset
        context["form_grade_pairs"] = form_grade_pairs

        return context
