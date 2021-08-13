from django.shortcuts import render
from login.views import LoginPermissionMixin
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib import messages

from .forms import SkillUploadForm

from members.models import MemberUser
from members.models import Member
from members.models import UserToMember
from members.models import UserRole
from .models import MemberToSkills
from .models import UserToSkills
from .models import Skill
import csv
import io
# Create your views here.

import logging
logger = logging.getLogger(__name__)

class CreateSkill(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Skill
    fields = ('name', 'description')

    def get_object(self, *args, **kwargs):
        obj = super(CreateSkill, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def dispatch(self, *args, **kwargs):
        return super(CreateSkill, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateSkill, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Skill'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save() 

        member_pk = self.kwargs.get('pk')
        member = MemberUser.objects.get(pk=member_pk)
        member_skill = UserToSkills()
        member_skill.skill = obj
        member_skill.member = member
        member_skill.save()

        success_url = "/profile/" + str(member_pk)
        return HttpResponseRedirect(success_url)

class AddSkill(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = UserToSkills
    fields = ('skill',)

    def get_object(self, *args, **kwargs):
        obj = super(AddSkill, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def dispatch(self, *args, **kwargs):
        return super(AddSkill, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddSkill, self).get_context_data(**kwargs)
        context['button_text'] = 'Add Skill'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user_pk = self.kwargs.get('pk')
        user = MemberUser.objects.get(pk=user_pk)
        obj.user = user
        obj.save() 

        success_url = "/profile/" + str(user_pk)
        return HttpResponseRedirect(success_url)

class AddMemberSkill(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = MemberToSkills
    fields = ('skill',)

    def get_object(self, *args, **kwargs):
        obj = super(AddMemberSkill, self).get_object(*args, **kwargs)
        
        try:
            user = MemberUser.objects.get(user=self.request.user)
            member = Member.objects.get(pk=self.kwargs.get('pk'))
            member_to_user = UserToMember.objects.get(member=member, user=user)
            user_role = UserRole.objects.get(member=member, user=user)
            if self.request.user.is_superuser:
                return obj
            if member_to_user.is_owner:
                return obj
            if user_role.permissions.is_member_admin or user_role.permissions.can_add_skills:
                return obj
            if user.is_wf_admin:
                return obj
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

    def dispatch(self, *args, **kwargs):
        return super(AddMemberSkill, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddMemberSkill, self).get_context_data(**kwargs)
        context['button_text'] = 'Add Skill'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        member_pk = self.kwargs.get('pk')
        member = Member.objects.get(pk=member_pk)
        obj.member = member
        obj.save() 

        success_url = "/member/" + str(member_pk)
        return HttpResponseRedirect(success_url)

class ViewSkill(LoginPermissionMixin, View):
    template_name = 'skills/skill.html'

    def get(self, request, pk):
        skill = Skill.objects.get(pk=pk)
        member_with_skill = MemberToSkills.objects.filter(skill=skill)
        users_with_skill = UserToSkills.objects.filter(skill=skill) 

        context = {
            'skill': skill,
            'members_with_skill': member_with_skill,
            'users_with_skill': users_with_skill
        }

        return render(request, self.template_name, context)

class MySkills(LoginPermissionMixin, View):
    template_name = 'skills/my_skills.html'

    def get(self, request, pk):
        user = MemberUser.objects.get(pk=pk)
        member_skills = UserToSkills.objects.filter(user=user)

        context = {
            'member_skills': member_skills,
            'profile': user
        }

        return render(request, self.template_name, context)

class MemberSkill(LoginPermissionMixin, View):
    template_name = 'skills/member_skills.html'

    def get(self, request, pk):
        member = Member.objects.get(pk=pk)
        member_skills = MemberToSkills.objects.filter(member=member)

        context = {
            'member_skills': member_skills,
            'member': member
        }

        return render(request, self.template_name, context)

class UploadSkills(LoginPermissionMixin, View):
    template_name = 'skills/upload_skills.html'

    def get(self, request):
        form = SkillUploadForm()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SkillUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)

            for line in csv.reader(io_string, delimiter=","):
                skill_name = line[0]
                count = Skill.objects.filter(name=skill_name).count()
                if count == 0:
                    skill = Skill()
                    skill.name = skill_name
                    skill.description = line[1]
                    skill.save()

        messages.add_message(request, messages.SUCCESS, "Your file has been uploaded successfully")
        return HttpResponseRedirect('/upload_skills')

class RemoveSkillFromUser(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = UserToSkills

    def get_context_data(self, **kwargs):
        context = super(RemoveSkillFromUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Remove Skill'
        return context
    
    def dispatch(self, *args, **kwargs):
        return super(RemoveSkillFromUser, self).dispatch(*args, **kwargs)
    
    def delete(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        user_pk = self.kwargs.get('user_pk')
        
        participant = UserToSkills.objects.get(pk=pk)
        participant.delete()

        success_url = "/profile/" + str(user_pk)
        return HttpResponseRedirect(success_url )

class RemoveSkillFromMember(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = MemberToSkills

    def get_context_data(self, **kwargs):
        context = super(RemoveSkillFromMember, self).get_context_data(**kwargs)
        context['button_text'] = 'Remove Skill'
        return context
    
    def dispatch(self, *args, **kwargs):
        return super(RemoveSkillFromMember, self).dispatch(*args, **kwargs)
    
    def delete(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        member_pk = self.kwargs.get('member_pk')
        
        participant = UserToMember.objects.get(pk=pk)
        participant.delete()

        success_url = "/member/" + str(member_pk)
        return HttpResponseRedirect(success_url)
    