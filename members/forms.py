from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from .models import Member
from .models import MemberUser
from .models import UserRole
from .models import Permissions

class ApplicationForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=255, error_messages={'required': 'Please enter your name'})
    email = forms.EmailField(label='Your Email', max_length=255)
    organization_name = forms.CharField(label='Organization Name', max_length=255)
    organization_email = forms.EmailField(label='Organization Email', max_length=255)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='New User Name', max_length=255)
    last_name = forms.CharField(label='New User Last Name', max_length=255)
    email = forms.EmailField(label="New User Email", max_length=255)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        

class RoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('user', 'permissions')

    def __init__(self, *args, **kwargs):
        member_pk = kwargs.pop('member_pk')
        super(RoleForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        self.fields['user'].queryset = MemberUser.objects.distinct().filter(usertomember__member__pk=member_pk)
        self.fields['permissions'].queryset = Permissions.objects.filter(member__pk=member_pk)

class UpdateRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('permissions',)

    def __init__(self, *args, **kwargs):
        member_pk = kwargs.pop('member_pk')
        super(UpdateRoleForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        
        self.fields['permissions'].queryset = Permissions.objects.filter(member__pk=member_pk)



