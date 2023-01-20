from django import forms

from accountant.models import Fee


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = "__all__"
        exclude = ["course"]
