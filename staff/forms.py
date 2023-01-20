from django import forms

from staff.models import Attendence


class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendence
        fields = ("student", "is_present")
