from django import forms

class IndustryUploadForm(forms.Form):
    file = forms.FileField()