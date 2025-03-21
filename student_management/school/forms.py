from django import forms
from .models import Attendance


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
