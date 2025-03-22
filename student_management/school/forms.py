from django import forms
from .models import Attendance, Grade


class AttendanceForm(forms.ModelForm):
    classstudent_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Attendance
        fields = ["status"]


class AttendanceFormSet(forms.BaseFormSet):
    def __init__(self, *args, attendances=None, **kwargs):
        super().__init__(*args, **kwargs)
        if attendances:
            self.attendances = attendances
            num_forms = min(len(self.forms), len(attendances))
            for i in range(num_forms):
                self.forms[i].initial = {
                    "classstudent_id": attendances[i].classstudent.id,
                    "status": attendances[i].status,
                }


class GradeForm(forms.ModelForm):
    classstudent_id = forms.IntegerField(widget=forms.HiddenInput())
    # subject_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Grade
        fields = [
            "oral_score",
            "fifteen_min_score",
            "one_period_score",
            "midterm_score",
            "final_score",
        ]


class GradeFormSet(forms.BaseFormSet):
    def __init__(self, *args, grades=None, **kwargs):
        super().__init__(*args, **kwargs)
        if grades:
            self.grades = grades
            num_forms = min(len(self.forms), len(grades))
            for i in range(num_forms):
                self.forms[i].initial = {
                    "classstudent_id": grades[i].classstudent.id,
                    # "subject_id": grades[i].subject.id,
                    "oral_score": grades[i].oral_score,
                    "fifteen_min_score": grades[i].fifteen_min_score,
                    "one_period_score": grades[i].one_period_score,
                    "midterm_score": grades[i].midterm_score,
                    "final_score": grades[i].final_score,
                }
