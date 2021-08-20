from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.contrib import auth
from django.contrib.auth.models import User
from login.views import LoginPermissionMixin
from login.views import WFAdminPermissionMixin
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponseRedirect
from django.views.decorators import csrf
from django.utils import timezone
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

##           FORMS              ##
from .forms import ApplicationForm
from .forms import SignUpForm
from .forms import MemberForm
from .forms import RoleForm
from .forms import UpdateRoleForm
##                              ##

##           MODELS             ##
from .models import ApplicationUpload, MemberUser, UserFlagMember, UserFlagUser
from .models import Member
from .models import UserToMember
from .models import UserRole
from .models import Permissions
from .models import Application as ApplicationModel
from skills.models import Skill
from skills.models import MemberToSkills
from skills.models import UserToSkills
from cal.models import Calendar
from cal.models import Filter
from events.models import Event
from events.models import Invitation
from events.models import Participants
from industries.models import MemberToIndustry, UsertoIndustry
##                              ##

import logging
logger = logging.getLogger(__name__)

class Index(View):
    template_name = 'members/index.html'

    def get(self, request):
        return render(request, self.template_name)

class MyProfile(LoginPermissionMixin, View):
    def get(self, request):
        member = MemberUser.objects.get(user=request.user.pk)
        id = member.pk
        
        address = '/profile/' + str(id)
        return HttpResponseRedirect(address)

class UserProfile(LoginPermissionMixin, View):
    template_name = 'members/profile.html'

    def get(self, request, pk):
        user = MemberUser.objects.get(pk=pk)
        calendar = Calendar.objects.get(user=user)
        filters = Filter.objects.filter(calendar__user=user)
        user_skills = UserToSkills.objects.filter(user=user)
        user_industries = UsertoIndustry.objects.filter(user=user)
        user_role = UserRole.objects.get(user=user)
        member_of = UserToMember.objects.filter(member_user=user)
        participations = Participants.objects.filter(member=user, events__date__gte=timezone.now())[:5]

        context = {
            'profile': user,
            'user_skills': user_skills,
            'user_industries': user_industries,
            'user_role': user_role,
            'calendar': calendar,
            'filters': filters,
            'member_of': member_of,
            'participations': participations
        }

        try:
            current_user = MemberUser.objects.get(user=self.request.user)
            user_flag_user = UserFlagUser.objects.get(flagged_user=user, user=current_user)
            if user_flag_user.flagged == True:
                context['flagged'] = True
        except UserFlagUser.DoesNotExist:
            context['flagged'] = False

        if request.user is not None:
            mId = request.user.pk
            user_member = MemberUser.objects.get(user=mId)
            if(user_member.pk == user.pk):
                context['my_profile'] = True
            else:
                context['my_profile'] = False

            active_user = MemberUser.objects.get(user=request.user)
            if active_user.is_wf_admin:
                context['admin'] = True
            else:
                context['admin'] = False

            if(request.user.is_superuser):
                context['admin'] = True
            else:
                context['admin'] = False
        
        return render(request, self.template_name, context)

class EditUser(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
    fields = (
        'first_name', 
        'last_name', 
        'job_title', 
        'address', 
        'address_2', 
        'city',
        'province',
        'country',
        'postal_code',
        'business_phone',
        'home_phone',
        'cell_phone',
        'email',
        'main_image'
        )

    def get_object(self, *args, **kwargs):
        obj = super(EditUser, self).get_object(*args, **kwargs)
        try:
            user = MemberUser.objects.get(user=self.request.user)
            admin_user = False
            active_user = MemberUser.objects.get(user=self.request.user)
            if active_user.is_wf_admin and active_user.member == user.member:
                admin_user = True  
            if user.pk == self.kwargs.get('pk') or self.request.user.is_superuser or admin_user:
                return obj
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Profile'
        return context

    def dispatch(self, *args, **kwargs):
        return super(EditUser, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        member_pk = self.kwargs.get('pk')

        success_url = '/profile/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class CreateUser(CreateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
    fields = (
        'first_name', 
        'last_name', 
        'job_title', 
        'address', 
        'address_2', 
        'city',
        'province',
        'country',
        'postal_code',
        'business_phone',
        'email',
        'website',
        'bio',
        'publicly_viewable',
        'main_image'
        )

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Profile'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        obj.user = user
        obj.membership_since = timezone.now()
        obj.save() 
        
        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.first_name + " " + obj.last_name
        calendar.member = obj

        calendar.save()

        success_url = "/pending_approval"
        return HttpResponseRedirect(success_url)

class CreateMemberChoice(View):
    
    def get(self, request):
        template_name = 'members/create_members.html'
        members = Member.objects.all()

        context = {
            'members': members
        }

        return render(request, template_name, context)


class CreateMemberProfile(CreateView):
    template_name = 'create_edit_model.html'
    model = MemberUser
    fields = (
        'first_name', 
        'last_name', 
        'job_title', 
        'address', 
        'address_2', 
        'city',
        'province',
        'country',
        'postal_code',
        'business_phone',
        'email',
        'website',
        'bio',
        'publicly_viewable',
        'main_image'
        )

    def get_context_data(self, **kwargs):
        context = super(CreateMemberProfile, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Profile'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = User.objects.get(pk=self.request.user.pk)
        obj.user = user
        obj.membership_since = timezone.now()
        obj.save() 
        
        calendar = Calendar()
        calendar.public = True
        calendar.name = "Calendar for " + obj.first_name + " " + obj.last_name
        calendar.member = obj

        calendar.save()

        success_url = "/pending_approval"
        return HttpResponseRedirect(success_url)

class MembersDirectory(View):
    template_name = 'members/members_directory.html'

    def get(self, request):
        members = Member.objects.all()
        context = {
            'members': members
        }
        
        return render(request, self.template_name, context)
        
class DirectorySearch(View):
    template_name='members/members_directory.html'

    def get(self, request, query):
        members = Member.objects.filter(Q(name__icontains=query))

        context = {
            'members': members,
            'query': query
        }

        return render(request, self.template_name, context)

class MemberView(View):
    template_name = 'members/member.html'

    def get(self, request, pk):
        member = Member.objects.get(pk=pk)
        member_skills = MemberToSkills.objects.filter(member=member)
        member_industries = MemberToIndustry.objects.filter(member=member)
        member_user_list = UserToMember.objects.filter(member=member)
        calendar = Calendar.objects.get(member=member)
        filters = Filter.objects.filter(calendar=calendar)
        upcoming_events = Event.objects.filter(calendar=calendar, date__gt=timezone.now()).order_by('-date')[:5]
        recent_events = Event.objects.filter(calendar=calendar, date__lt=timezone.now()).order_by('date')[:5]


        context = {
            'member': member,
            'member_skills': member_skills,
            'member_industries': member_industries,
            'member_user_list': member_user_list,
            'filters': filters,
            'calendar': calendar,
            'upcoming_events': upcoming_events,
            'recent_events': recent_events
        }

        try:
            current_user = MemberUser.objects.get(user=self.request.user)
            user_flag_member = UserFlagMember.objects.get(member=member, user=current_user)
            if user_flag_member.flagged == True:
                context['flagged'] = True
        except UserFlagMember.DoesNotExist:
            context['flagged'] = False

        if request.user.is_authenticated == True:
            user_member = MemberUser.objects.get(user=request.user.pk)
            user_to_member = UserToMember.objects.get(member_user__user=request.user.pk)
            context['is_owner'] = user_to_member.is_owner
            if user_to_member.member == member:
                user_role = UserRole.objects.get(user=user_member)
                context['member_admin'] = user_role.permissions.is_member_admin
                context['member_of'] = True
            else:
                context['member_admin'] = False
                context['member_of'] = False

        return render(request, self.template_name, context)

class EditMember(UpdateView):
    template_name = 'create_edit_model.html'
    model = Member
    form_class = MemberForm

    def get_object(self, *args, **kwargs):
        obj = super(EditMember, self).get_object(*args, **kwargs)
        try:
            admin_user = False
            is_member = False
            user = MemberUser.objects.get(user=self.request.user)
            user_to_member = UserToMember.objects.get(member_user__user=self.request.user, member=obj)
            user_role = UserRole.objects.get(user=user, member=obj)
            if user_to_member.member == obj:
                is_member = True
            if is_member and (user_role.permissions.is_member_admin or user_role.permissions.can_edit_company_profile):
                admin_user = True
            if user.pk == self.kwargs.get('pk') or self.request.user.is_superuser or admin_user or user.is_wf_admin:
                return obj
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(EditMember, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Member Profile'
        return context

    def dispatch(self, *args, **kwargs):
        return super(EditMember, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        member_pk = self.kwargs.get('pk')

        success_url = '/member/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class EditMembersList(LoginPermissionMixin, View):
    template_name="create_edit_model.html"

    def get(self, request, pk):
        MemberUserFormSet = inlineformset_factory(Member, UserToMember, fields=('member_user',))
        member = Member.objects.get(pk=pk)
        formset = MemberUserFormSet(instance=member)

        context={
            'form': formset,
            'button_text': "Update Member List",
            'title': member.name
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        logger.error(pk)
        MemberUserFormSet = inlineformset_factory(Member, UserToMember, fields=('member_user',))
        member = Member.objects.get(pk=pk)
        formset = MemberUserFormSet(request.POST, request.FILES, instance=member)

        success_url = '/member/' + str(pk)
        if formset.is_valid():
            formset.save()
        else:
            return HttpResponseRedirect(success_url)
        return HttpResponseRedirect(success_url)

class CreatePermissions(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Permissions
    fields = (
        'role_title',
        'is_member_admin',
        'can_add_calendar_events',
        'can_edit_company_profile',
        'can_add_employees',
        'can_delete_posts',
        'can_edit_own_profile',
    )

    def get_context_data(self, **kwargs):
        context = super(CreatePermissions, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Role'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.kwargs.get('member_pk')
        member = Member.objects.get(pk=pk)
        obj.member = member
        try:
            user = MemberUser.objects.get(user=self.request.user)
            user_to_member = UserToMember.objects.get(member_user=user, member=member)
            role = UserRole.objects.get(member=member, user=user)
            
            if user.is_wf_admin or self.request.user.is_superuser or user_to_member.is_owner or role.permissions.is_member_admin:
                obj.save() 
                success_url = "/permissions/" + str(pk)
                return HttpResponseRedirect(success_url)
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()
        

class EditPermissions(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Permissions
    fields = (
        'role_title',
        'is_member_admin',
        'can_add_calendar_events',
        'can_edit_company_profile',
        'can_add_employees',
        'can_delete_posts',
        'can_edit_own_profile',
    )

    def get_object(self, *args, **kwargs):
        obj = super(EditPermissions, self).get_object(*args, **kwargs)
        pk = self.kwargs.get('member_pk')
        member = Member.objects.get(pk=pk)
        try:
            user = MemberUser.objects.get(user=self.request.user)
            user_to_member = UserToMember.objects.get(member_user=user, member=member)
            role = UserRole.objects.get(member=member, user=user)
            
            if user.is_wf_admin or self.request.user.is_superuser or user_to_member.is_owner or role.permissions.is_member_admin:
                return obj        
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(EditPermissions, self).get_context_data(**kwargs)
        context['button_text'] = 'Edit Permissions'
        return context

    def dispatch(self, *args, **kwargs):
        return super(EditPermissions, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        pk = self.kwargs.get('member_pk')

        success_url = '/permissions/' + str(pk)
        return HttpResponseRedirect(success_url)

class PermissionsView(View):
    template_name = 'members/permissions.html'

    def get(self, request, pk):
        permissions = Permissions.objects.filter(member__pk=pk)

        logger.error(permissions.count())

        context = {
            'permissions': permissions
        }

        if permissions.count() > 0:
            member = permissions[0].member
            context['member_pk'] = member.pk
            context['member_name'] = member.name 

        return render(request, self.template_name, context)

class AssignRoles(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = UserRole
    form_class = RoleForm

    def get_context_data(self, **kwargs):
        context = super(AssignRoles, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Role'
        return context

    def get_form_kwargs(self):
        kwargs = super(AssignRoles, self).get_form_kwargs()
        kwargs['member_pk'] = self.kwargs.get('member_pk')
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.kwargs.get('member_pk')
        member = Member.objects.get(pk=pk)
        obj.member = member

        try:
            user = MemberUser.objects.get(user=self.request.user)
            user_to_member = UserToMember.objects.get(member_user=user, member=member)
            role = UserRole.objects.get(member=member, user=user)
            
            if user.is_wf_admin or self.request.user.is_superuser or user_to_member.is_owner or role.permissions.is_member_admin:
                target_user = obj.user
                if UserRole.objects.filter(user=target_user, member=member).exists():
                    old_role = UserRole.objects.get(user=target_user, member=member)
                    old_role.permissions = obj.permissions
                    old_role.save()
                else:
                    obj.save() 
                success_url = "/roles/" + str(pk)
                return HttpResponseRedirect(success_url)
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

class UpdateRoles(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = UserRole
    form_class = UpdateRoleForm

    def get_form_kwargs(self):
        kwargs = super(UpdateRoles, self).get_form_kwargs()
        kwargs['member_pk'] = self.kwargs.get('member_pk')
        return kwargs

    def get_object(self, *args, **kwargs):
        obj = super(UpdateRoles, self).get_object(*args, **kwargs)
        pk = self.kwargs.get('member_pk')
        member = Member.objects.get(pk=pk)
        try:
            user = MemberUser.objects.get(user=self.request.user)
            user_to_member = UserToMember.objects.get(member_user=user, member=member)
            role = UserRole.objects.get(member=member, user=user)
            
            if user.is_wf_admin or self.request.user.is_superuser or user_to_member.is_owner or role.permissions.is_member_admin:
                return obj        
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(UpdateRoles, self).get_context_data(**kwargs)
        title = self.object.user
        context['button_text'] = 'Edit Permissions'
        context['title'] = title
        return context

    def dispatch(self, *args, **kwargs):
        return super(UpdateRoles, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        pk = self.kwargs.get('member_pk')

        success_url = '/roles/' + str(pk)
        return HttpResponseRedirect(success_url)

class Roles(View):
    template_name = 'members/roles.html'

    def get(self, request, pk):
        permissions = Permissions.objects.filter(member__pk=pk)

        context = {
            'permissions': permissions
        }

        if permissions.count() > 0:
            member = permissions[0].member
            context['member_pk'] = member.pk
            context['member_name'] = member.name
        

        return render(request, self.template_name, context)

class RolesEditAll(LoginPermissionMixin, View):
    template_name="create_edit_model.html"

    def get(self, request, pk):
        RoleFormSet = inlineformset_factory(Member, UserRole, fields=('user', 'permissions',))
        member = Member.objects.get(pk=pk)
        formset = RoleFormSet(instance=member)

        context={
            'form': formset,
            'button_text': "Update Role List",
            'title': member.name
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        RoleFormSet = inlineformset_factory(Member, UserRole, fields=('user', 'permissions',))
        member = Member.objects.get(pk=pk)
        formset = RoleFormSet(request.POST, request.FILES, instance=member)

        success_url = '/roles/' + str(pk)
        if formset.is_valid():
            formset.save()
        else:
            messages.add_message(request, messages.ERROR, "Cannot enter blank or duplicates.")
            return HttpResponseRedirect(self.request.path_info)
        
        return HttpResponseRedirect(success_url)

class Invites(LoginPermissionMixin, View):
    template_name = 'members/invites.html'

    def get_object(self, *args, **kwargs):
        obj = super(Invites, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            if member.pk != self.kwargs.get('pk'):
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get(self, request, pk):
        member = MemberUser.objects.get(pk=pk)

        # PERMISSIONS #
        my_member = MemberUser.objects.get(user=request.user)

        if member != my_member:
            raise PermissionDenied()

        invites = Invitation.objects.filter(member=member)
        participations = Participants.objects.filter(member=member)

        context = {
            'invites': invites,
            'profile': member,
            'participations': participations
        }

        return render(request, self.template_name, context)

class SignUp(WFAdminPermissionMixin, CreateView):
    template_name = 'members/signup.html'
    form_class = SignUpForm

    def get_object(self, *args, **kwargs):
        obj = super(SignUp, self).get_object(*args, **kwargs)
        try:
            member_pk = self.kwargs.get('pk')
            member_user = MemberUser.objects.get(user=self.request.user)
            member = Member.objects.get(pk=member_pk)
            if member != member_user.member:
                raise PermissionDenied()
        except Member.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['member_list'] = Member.objects.filter(pk=self.kwargs.get('pk'))
        context['button_text'] = 'Create Member'
        return context

    def dispatch(self, *args, **kwargs):
        return super(SignUp, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        member_pk = self.kwargs.get('pk')
        member = Member.objects.get(pk=member_pk)
        member_user = MemberUser()
        if MemberUser.objects.filter(email=member_user.email).exists():
            member_user = MemberUser.objects.get(email=member_user.email)
        else:
            member_user = MemberUser()
            member_user.first_name = form.cleaned_data['first_name']
            member_user.last_name = form.cleaned_data['last_name']
            member_user.member = member
            member_user.user = obj
            member_user.save()

            calendar = Calendar()
            calendar.user = member_user
            calendar.name = member_user.first_name + member_user.last_name + "s Calendar"
            calendar.save()

        user_to_member = UserToMember()
        user_to_member.member = member
        user_to_member.member_user = member_user
        user_to_member.save()

        permissions = Permissions()
        permissions.title = "New Permissions"
        permissions.save()

        user_role = UserRole()
        user_role.user = member_user
        user_role.permissions = permissions
        user_role.save()

        success_url = '/member/' + str(member_pk)
        return HttpResponseRedirect(success_url)

class Approval(View):
    template_name = 'members/pending_approval.html'

    def get(self, request):
        return render(request, self.template_name, {})

class UpdatePassword(PasswordChangeView):
    template_name = 'members/controls/update_password.html'
    success_url = '/my_profile'
    form_class = PasswordChangeForm

class Application(CreateView):
    template_name = 'create_edit_model.html'
    model = ApplicationModel
    fields = ('surname', 'first_name', 'email', 'title',
    'business_name', 'business_website', 'address', 'city', 'province', 'postal_code',
    'birthdate', 'phone_number', 'referred_by', 'other')

    def get_context_data(self, **kwargs):
        context = super(Application, self).get_context_data(**kwargs)
        context['button_text'] = 'Submit Application'
        return context

    def get_form(self, form_class=None):
        form = super(Application, self).get_form(form_class)
        form.fields['surname'].required = True
        form.fields['first_name'].required = True
        form.fields['phone_number'].required = True
        return form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save() 
        messages.add_message(self.request, messages.SUCCESS, "Thank you for the application. Someone from Wayfinders will follow up with you soon")
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please correct the form below.")
        return super().form_invalid(form)

class ApplicationSubmission(CreateView):
    template_name = 'create_edit_model.html'
    model = ApplicationUpload
    fields = ('file',)
    

    def get_context_data(self, **kwargs):
        context = super(ApplicationSubmission, self).get_context_data(**kwargs)
        context['button_text'] = 'Submit'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        messages.add_message(self.request, messages.SUCCESS, "Thank you for the application. Someone from Wayfinders will follow up with you soon")
        success_url = '/'
        return HttpResponseRedirect(success_url)

class ApplicationChoice(View):
    template_name = 'members/application_choice.html'

    def get(self, request):
        return render(request, self.template_name)

class ApplicationView(View):
    template_name = 'members/application_view.html'

    def get(self, request):
        applications = ApplicationModel.objects.all()
        context = {
            'applications': applications
        }
        
        return render(request, self.template_name, context)

class ApplicationDetails(View):
    template_name = 'members/application_details.html'

    def get(self, request, pk):
        application = ApplicationModel.objects.get(pk=pk)
        context = {
            'application': application
        }
        
        return render(request, self.template_name, context)


class ApplicationFiles(View):
    template_name = 'members/application_files.html'

    def get(self, request):
        applications = ApplicationUpload.objects.all()
        context = {
            'applications': applications
        }
        
        return render(request, self.template_name, context)

class ApplicationSubmit(View):
    def post(self, request, pk, approved, *args, **kwargs):
        success_url = "/application_directory"
        application = ApplicationModel.objects.get(pk=pk)
        application.processed = True

        if approved == "true":
            application.approved = True

        application.save()
       
        return HttpResponseRedirect(success_url)

class ViewApplications(View):
    template_name = 'members/applications.html'

    def get(self, request):
        applications = ApplicationModel.objects.all().order_by('-date')

        context = {
            'applications': applications
        }

        return render(request, self.template_name, context)

class ViewApplicationUploads(View):
    template_name = 'members/applications.html'

    def get(self, request):
        applications = ApplicationUpload.objects.all().order_by('-date')

        context = {
            'application_uploads': applications
        }

        return render(request, self.template_name, context)

class ApplicationFileDetails(View):
    template_name = 'members/application_file.html'

    def get(self, request, pk):
        application = ApplicationUpload.objects.get(pk=pk)

        context = {
            'application': application
        }

        return render(request, self.template_name, context)

class ApplicationFileSubmit(View):
    def post(self, request, pk, approved, *args, **kwargs):
            success_url = "/application_files"
            application = ApplicationUpload.objects.get(pk=pk)
            application.processed = True

            if approved == "true":
                application.approved = True

            application.save()
        
            return HttpResponseRedirect(success_url)


class ViewFlaggedUsers(View):
    template_name = 'members/user_flags.html'

    def get(self, request):
        users = MemberUser.objects.filter(number_of_flags__gt=0).distinct().order_by('number_of_flags')

        context = {
            'users': users
        }

        return render(request, self.template_name, context)

class ViewFlaggedMembers(View):
    template_name = 'members/user_flags.html'

    def get(self, request):
        members = Member.objects.filter(number_of_flags__gt=0).distinct().order_by('number_of_flags')

        context = {
            'members': members
        }

        return render(request, self.template_name, context)


@csrf.csrf_exempt
def flag_user(request, member_pk, flagged_member_pk):
    member = MemberUser.objects.get(pk=member_pk)
    flagged_member = MemberUser.objects.get(pk=flagged_member_pk)
    try:
        user_flag_user = UserFlagUser.objects.get(user=member, flagged_user=flagged_member)
        if user_flag_user.flagged is True:
            user_flag_user.flagged = False
            flagged_member.number_of_flags -=1
        else:
            user_flag_user.flagged = True
            flagged_member.number_of_flags += 1
        flagged_member.save()
        user_flag_user.save()
    except UserFlagUser.DoesNotExist:
        user_flag_user = UserFlagUser()
        user_flag_user.flagged = True
        user_flag_user.user = member
        user_flag_user.flagged_user = flagged_member_pk
        user_flag_user.save()

        flagged_member.number_of_flags += 1
        flagged_member.save()

    success_url = "/profile/" + str(flagged_member_pk)
    return HttpResponseRedirect(success_url)


@csrf.csrf_exempt
def flag_member(request, member_pk, flagged_member_pk):
    member = MemberUser.objects.get(pk=member_pk)
    flagged_member = Member.objects.get(pk=flagged_member_pk)
    try:
        user_flag_member = UserFlagMember.objects.get(user=member, member=flagged_member)
        if user_flag_member.flagged is True:
            user_flag_member.flagged = False
            flagged_member.number_of_flags -=1
        else:
            user_flag_member.flagged = True
            flagged_member.number_of_flags += 1
        flagged_member.save()
        user_flag_member.save()
    except UserFlagMember.DoesNotExist:
        user_flag_member = UserFlagMember()
        user_flag_member.flagged = True
        user_flag_member.user = member
        user_flag_member.member = flagged_member
        user_flag_member.save()

        flagged_member.number_of_flags += 1
        flagged_member.save()

    success_url = "/member/" + str(flagged_member_pk)
    return HttpResponseRedirect(success_url)