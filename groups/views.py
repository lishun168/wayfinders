from django.shortcuts import render
from django.views import View
from .models import Groups, GroupToMember
from members.models import MemberUser, UserRole, Member
from cal.models import Calendar
from login.views import LoginPermissionMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied 
from django.utils import timezone
from django.views.generic.edit import UpdateView, CreateView, DeleteView


class CreateGroup(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Groups
    fields = '__all__'

    def get_object(self, *args, **kwargs):
        obj = super(CreateGroup, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def dispatch(self, *args, **kwargs):
        return super(CreateGroup, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Group'
        return context

    def form_valid(self, form):

        obj = form.save(commit=False)
        member_pk = self.kwargs.get('pk')
        member = MemberUser.objects.get(pk=member_pk)
        obj.save() 
        role = UserRole()
        role.title = obj.name + " admin"
        role.can_create_forum_group = True
        role.can_post_to_forums = True
        role.can_add_calendar_events = True
        role.can_see_all_members = True
        role.can_edit_company_profile = True
        role.can_see_company_console = True
        role.can_add_employees = True
        role.can_delete_posts = True
        role.is_account_manager = True
        role.is_calendar_manager = True
        role.save()

        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.name 
        calendar.company = obj

        member_company = Member()
        member_company.role = role
        member_company.member = member
        member_company.company = obj
        member_company.member_since = timezone.now()
        member_company.save()
        
        group_pk = obj.pk

        success_url = "/group/" + str(group_pk)
        return HttpResponseRedirect(success_url)

class LeaveGroup(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = Member
    fields = '__all__'

    def get_object(self, *args, **kwargs):
        obj = super(LeaveGroup, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            member_company = Member.objects.get(pk=self.kwargs.get('pk'))
            if member_company.member != member:
                raise PermissionDenied()
        except Member.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(LeaveGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Confirm to Leave the Group'
        return context

    def delete(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        my_object = self.object
        self.object.delete()
        
        members_left = Member.objects.filter(company=my_object.company)
        
        if not members_left:
            group = MemberUser.objects.get(pk=my_object.company.pk)
            group.public = False
            group.save()
        else:
            oldest_member = None
            oldest_member_date = timezone.now()
            current_admin = False
            for member in members_left:
                if member.role.is_account_manager:
                    current_admin = True
                if member.member_since < timezone.now():
                    oldest_member_date = timezone.now()
                    oldest_member = member
            if current_admin is False:
                oldest_member.role.is_account_manager = True
                oldest_member.save()

        member = MemberUser.objects.get(user=request.user)
        success_url = "/profile/" + str(member.pk)
        return HttpResponseRedirect(success_url)

class EditGroup(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Groups
    fields = '__all__'

    def get_object(self, *args, **kwargs):
        obj = super(EditGroup, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            group = MemberUser.objects.get(pk=self.kwargs.get('pk'))
            member_group = Member.objects.get(member=member, company=group)
            if member_group.role.can_edit_company_profile is False:
                raise PermissionDenied()
        except (MemberUser.DoesNotExist, MemberUser.DoesNotExist, Member.DoesNotExist):
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditGroup, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Group'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save() 

        pk=obj.pk

        success_url = "/group/" + str(pk)
        return HttpResponseRedirect(success_url)

class MyGroups(LoginPermissionMixin, View):
    template_name = 'members/my_groups.html'

    def get(self, request, pk):
        member = MemberUser.objects.get(pk=pk)
        member_groups = GroupToMember.objects.filter(member=member)

        context = {
            'member_groups': member_groups,
            'profile': member
        }

        return render(request, self.template_name, context)
