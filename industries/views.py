from django.shortcuts import render
from login.views import LoginPermissionMixin
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.contrib import messages
import csv
import io

from .forms import IndustryUploadForm

from .models import Industry
from .models import MemberToIndustry
from .models import UsertoIndustry
from members.models import MemberUser
from members.models import Member
from members.models import UserToMember
from members.models import UserRole

import logging
logger = logging.getLogger(__name__)

class ViewIndustry(LoginPermissionMixin, View):
    template_name = 'industries/industry.html'

    def get(self, request, pk):
        industry = Industry.objects.get(pk=pk)
        members_in_industry = MemberToIndustry.objects.filter(industry=industry)
        users_in_industry = UsertoIndustry.objects.filter(industry=industry) 

        context = {
            'industry': industry,
            'members_in_industry': members_in_industry,
            'users_in_industry': users_in_industry
        }

        return render(request, self.template_name, context)

class AddIndustry(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = UsertoIndustry
    fields = ('industry',)

    def get_object(self, *args, **kwargs):
        obj = super(AddIndustry, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def dispatch(self, *args, **kwargs):
        return super(AddIndustry, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddIndustry, self).get_context_data(**kwargs)
        context['button_text'] = 'Add Industry'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user_pk = self.kwargs.get('pk')
        user = MemberUser.objects.get(pk=user_pk)
        obj.user = user
        obj.save() 

        success_url = "/profile/" + str(user_pk)
        return HttpResponseRedirect(success_url)

class AddMemberIndustry(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = MemberToIndustry
    fields = ('industry',)

    def get_object(self, *args, **kwargs):
        obj = super(AddMemberIndustry, self).get_object(*args, **kwargs)
        
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
        return super(AddMemberIndustry, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddMemberIndustry, self).get_context_data(**kwargs)
        context['button_text'] = 'Add Industry'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        member_pk = self.kwargs.get('pk')
        member = Member.objects.get(pk=member_pk)
        obj.member = member
        obj.save() 

        success_url = "/member/" + str(member_pk)
        return HttpResponseRedirect(success_url)

class MyIndustries(LoginPermissionMixin, View):
    template_name = 'industries/my_industries.html'

    def get(self, request, pk):
        user = MemberUser.objects.get(pk=pk)
        user_industries = UsertoIndustry.objects.filter(user=user)

        context = {
            'user_industries': user_industries,
            'profile': user
        }

        return render(request, self.template_name, context)

class MemberIndustries(LoginPermissionMixin, View):
    template_name = 'industries/member_industries.html'

    def get(self, request, pk):
        member = Member.objects.get(pk=pk)
        member_industries = MemberToIndustry.objects.filter(member=member)

        context = {
            'member_industries': member_industries,
            'member': member
        }

        return render(request, self.template_name, context)
    
class UploadIndustries(LoginPermissionMixin, View):
    template_name = 'industries/upload_industries.html'

    def get(self, request):
        form = IndustryUploadForm()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = IndustryUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)

            for line in csv.reader(io_string, delimiter=","):
                industry_name = line[0]
                count = Industry.objects.filter(name=industry_name).count()
                if count == 0:
                    industry = Industry()
                    industry.name = industry_name
                    industry.description = line[1]
                    industry.save()

        messages.add_message(request, messages.SUCCESS, "Your file has been uploaded successfully")
        return HttpResponseRedirect('/upload_industries')

class RemoveIndustryFromUser(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = UsertoIndustry

    def get_context_data(self, **kwargs):
        context = super(RemoveIndustryFromUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Remove Industry'
        return context
    
    def dispatch(self, *args, **kwargs):
        return super(RemoveIndustryFromUser, self).dispatch(*args, **kwargs)
    
    def delete(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        user_pk = self.kwargs.get('user_pk')
        
        participant = UsertoIndustry.objects.get(pk=pk)
        participant.delete()

        success_url = "/profile/" + str(user_pk)
        return HttpResponseRedirect(success_url )

class RemoveIndustryFromMember(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = MemberToIndustry

    def get_context_data(self, **kwargs):
        context = super(RemoveIndustryFromMember, self).get_context_data(**kwargs)
        context['button_text'] = 'Remove Industry'
        return context
    
    def dispatch(self, *args, **kwargs):
        return super(RemoveIndustryFromMember, self).dispatch(*args, **kwargs)
    
    def delete(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        member_pk = self.kwargs.get('member_pk')
        
        participant = MemberToIndustry.objects.get(pk=pk)
        participant.delete()

        success_url = "/member/" + str(member_pk)
        return HttpResponseRedirect(success_url)

