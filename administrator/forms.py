from django import forms
from phonenumber_field.formfields import RegionalPhoneNumberWidget

from administrator.models import (
    AcademicSession,
    Address,
    Assign,
    Class,
    Course,
    Department,
    Staff,
    Student,
    Subject,
    TimeSlot,
)


class AcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = "__all__"
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class AssignForm(forms.ModelForm):
    class Meta:
        model = Assign
        fields = "__all__"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "current_class",
            "gender",
            "dob",
            "fathers_name",
            "fathers_contact_no",
            "mothers_name",
            "mothers_contact_no",
            "document",
        )
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = (
            "gender",
            "dob",
            "fathers_name",
            "document",
        )
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
        }
