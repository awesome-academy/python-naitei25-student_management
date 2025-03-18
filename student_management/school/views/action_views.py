from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from school.models import Student, ClassStudent, Attendance
from school.forms import AttendanceForm, AttendanceFormSet
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

                # Attendance.objects.filter(
                #     classstudent__id=classstudent_id, date=now().date()
                # ).update(status=status)

                attendance, created = Attendance.objects.update_or_create(
                    classstudent__id=classstudent_id,
                    date=now().date(),
                    defaults={"status": status},
                )

                attendance.save()

    return redirect("attendance-tracking", class_id, semester_id)
