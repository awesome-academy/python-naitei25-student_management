from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from school.models import Student, ClassStudent, Attendance, Grade
from school.forms import AttendanceForm, GradeForm
from django.utils.timezone import now


@login_required
def post_attendance(request):
    class_id = request.session.get("class_id")
    semester_id = request.session.get("semester_id")

    if request.method == "POST":
        students = Student.objects.all()
        AttendanceFormSetFactory = formset_factory(AttendanceForm)
        formset = AttendanceFormSetFactory(request.POST)

        if formset.is_valid():
            for form in formset:
                classstudent_id = form.cleaned_data["classstudent_id"]
                status = form.cleaned_data["status"]

                attendance, created = Attendance.objects.update_or_create(
                    classstudent__id=classstudent_id,
                    date=now().date(),
                    defaults={"status": status},
                )

                attendance.save()

    return redirect("attendance-tracking", class_id, semester_id)


@login_required
def post_grade(request):
    class_id = request.session.get("class_id")
    semester_id = request.session.get("semester_id")
    subject_id = request.session.get("subject_id")

    if request.method == "POST":
        students = Student.objects.all()
        GradeFormSetFactory = formset_factory(GradeForm)
        formset = GradeFormSetFactory(request.POST)

        if formset.is_valid():
            for form in formset:
                classstudent_id = form.cleaned_data["classstudent_id"]
                oral_score = form.cleaned_data["oral_score"]
                fifteen_min_score = form.cleaned_data["fifteen_min_score"]
                one_period_score = form.cleaned_data["one_period_score"]
                midterm_score = form.cleaned_data["midterm_score"]
                final_score = form.cleaned_data["final_score"]

                grade, created = Grade.objects.update_or_create(
                    classstudent__id=classstudent_id,
                    subject__id=subject_id,
                    defaults={
                        "oral_score": oral_score,
                        "fifteen_min_score": fifteen_min_score,
                        "one_period_score": one_period_score,
                        "midterm_score": midterm_score,
                        "final_score": final_score,
                    },
                )

                grade.save()

    return redirect("grade", class_id, semester_id, subject_id)
