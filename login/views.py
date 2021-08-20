from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from members.models import MemberUser
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from cal.models import Calendar

class LoginPermissionMixin(object):
    def has_permissions(self):
        if self.request.user.is_authenticated == False:
            return False
        try:
            member = MemberUser.objects.get(user=self.request.user)
        except MemberUser.DoesNotExist:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return HttpResponseRedirect('/login_page')
        return super(LoginPermissionMixin, self).dispatch(request, *args, **kwargs)

class WFAdminPermissionMixin(object):
    def has_permissions(self):
        if self.request.user.is_authenticated == False:
            return False
        elif self.request.user.is_superuser == True:
            return True
        else:
            member = MemberUser.objects.get(user=self.request.user)
            if member.is_wf_admin == False:
                return False
            return True
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return HttpResponseRedirect('/')
        return super(WFAdminPermissionMixin, self).dispatch(request, *args, **kwargs)


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = 'login/login.html'
    success_url = '/login'
    success_message = 'Thank you for logging in'

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        try:
            member_user = MemberUser.objects.get(user=user)
            calendar = Calendar.objects.get(user=member_user)
            cal_url = "/calendar/" + str(calendar.pk)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            return HttpResponseRedirect(cal_url)
        except MemberUser.DoesNotExist:
            return HttpResponseRedirect("/  ")
    else:
        messages.add_message(request, messages.ERROR, "Your username and/or password is incorrect.")
        return HttpResponseRedirect('/login_page')



