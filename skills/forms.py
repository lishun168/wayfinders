from django import forms

class SkillUploadForm(forms.Form):
    file = forms.FileField()