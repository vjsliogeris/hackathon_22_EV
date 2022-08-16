from django import forms

class PayslipForm(forms.Form):
    payslip_doc = forms.FileField()
