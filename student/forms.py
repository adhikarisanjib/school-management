from django import forms


class AmountForm(forms.Form):
    pay_amount = forms.DecimalField(widget=forms.NumberInput())
