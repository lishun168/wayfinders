from django import forms

class SearchForm(forms.Form):
    subject = forms.CharField(label="Discussion Subject Contains", max_length=100, required=False)
    contains = forms.CharField(label="Posts Contain", max_length=100, required=False)
    likes = forms.BooleanField(label="Most Liked", initial=False, required=False)
    sticky = forms.BooleanField(label="Sticky on Top", initial=True, required=False)

