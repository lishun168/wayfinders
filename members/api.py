from rest_framework import viewsets
from .serializers import MemberSerializer
from .serializers import MemberUserSerializer
from .serializers import UserToMemberSerializer
from .serializers import PermissionsSerializer
from .serializers import UserRoleSerializer
from .serializers import GallerySerializer
from .serializers import ApplicationSerializer
from .models import Member
from .models import MemberUser
from .models import UserToMember
from .models import Permissions
from .models import UserRole
from .models import Gallery
from .models import Application
from wayfinders.functions import add_to_queryset
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token

import logging

logger = logging.getLogger('members.api')


class MemberAPI(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    http_method_names = ['get', 'head', 'post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        description = self.request.query_params.get('description')
        main_image = self.request.query_params.get('main_image')
        public = self.request.query_params.get('public')  # bool
        logo = self.request.query_params.get('logo')
        website = self.request.query_params.get('website')
        business_phone = self.request.query_params.get('business_phone')
        address = self.request.query_params.get('address')
        address_2 = self.request.query_params.get('address_2')
        city = self.request.query_params.get('city')
        province = self.request.query_params.get('province')
        country = self.request.query_params.get('country')
        postal_code = self.request.query_params.get('postal_code')
        membership_expiry = self.request.query_params.get('membership_expiry')
        membership_since = self.request.query_params.get('membership_since')
        business_email = self.request.query_params.get('business_email')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'description__icontains', description)
        add_to_queryset(queryset_params, 'main_image__icontains', main_image)
        add_to_queryset(queryset_params, 'logo__icontains', logo)
        add_to_queryset(queryset_params, 'website__icontains', website)
        add_to_queryset(queryset_params, 'business_phone__icontains', business_phone)
        add_to_queryset(queryset_params, 'address__icontains', address)
        add_to_queryset(queryset_params, 'address_2__icontains', address_2)
        add_to_queryset(queryset_params, 'city__icontains', city)
        add_to_queryset(queryset_params, 'province__icontains', province)
        add_to_queryset(queryset_params, 'country__icontains', country)
        add_to_queryset(queryset_params, 'postal_code__icontains', postal_code)
        add_to_queryset(queryset_params, 'membership_expiry__icontains', membership_expiry)
        add_to_queryset(queryset_params, 'membership_since__icontains', membership_since)
        add_to_queryset(queryset_params, 'business_email__icontains', business_email)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()


class MemberUserAPI(viewsets.ModelViewSet):
    serializer_class = MemberUserSerializer
    http_method_names = ['get', 'head', 'post', 'patch']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        primary_member = self.request.query_params.get('primary_member')
        first_name = self.request.query_params.get('first_name')
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        address = self.request.query_params.get('address')
        address_2 = self.request.query_params.get('address_2')
        city = self.request.query_params.get('city')
        province = self.request.query_params.get('province')
        country = self.request.query_params.get('country')
        postal_code = self.request.query_params.get('postal_code')
        business_phone = self.request.query_params.get('business_phone')
        home_phone = self.request.query_params.get('home_phone')
        cell_phone = self.request.query_params.get('cell_phone')
        publicly_viewable = self.request.query_params.get('publicly_viewable')  # bool
        membership_since = self.request.query_params.get('membership_since')
        main_image = self.request.query_params.get('main_image')
        is_focum_mod = self.request.query_params.get('is_focum_mod')  # bool
        primary_member_id = self.request.query_params.get('primary_member_id')  # int
        search_tag_id = self.request.query_params.get('search_tag_id')  # int
        user_id = self.request.query_params.get('user_id')  # int
        is_wf_admin = self.request.query_params.get('is_wf_admin')  # bool

        queryset_params = {}
        add_to_queryset(queryset_params, 'primary_member__pk', primary_member)
        add_to_queryset(queryset_params, 'first_name', first_name)
        add_to_queryset(queryset_params, 'last_name', last_name)
        add_to_queryset(queryset_params, 'email__icontains', email)
        add_to_queryset(queryset_params, 'address__icontains', address)
        add_to_queryset(queryset_params, 'address_2__icontains', address_2)
        add_to_queryset(queryset_params, 'city', city)
        add_to_queryset(queryset_params, 'province', province)
        add_to_queryset(queryset_params, 'country', country)
        add_to_queryset(queryset_params, 'postal_code', postal_code)
        add_to_queryset(queryset_params, 'business_phone', business_phone)
        add_to_queryset(queryset_params, 'home_phone', home_phone)
        add_to_queryset(queryset_params, 'cell_phone', cell_phone)
        add_to_queryset(queryset_params, 'membership_since__icontains', membership_since)
        add_to_queryset(queryset_params, 'main_image__icontains', main_image)
        add_to_queryset(queryset_params, 'primary_member_id', primary_member_id)
        add_to_queryset(queryset_params, 'search_tag_id', search_tag_id)
        add_to_queryset(queryset_params, 'user_id', user_id)

        if (publicly_viewable == "true"):
            add_to_queryset(queryset_params, 'publicly_viewable', True)
        elif (publicly_viewable == "false"):
            add_to_queryset(queryset_params, 'publicly_viewable', False)

        if (is_focum_mod == "true"):
            add_to_queryset(queryset_params, 'is_focum_mod', True)
        elif (is_focum_mod == "false"):
            add_to_queryset(queryset_params, 'is_focum_mod', False)

        if (is_wf_admin == "true"):
            add_to_queryset(queryset_params, 'is_wf_admin', True)
        elif (is_wf_admin == "false"):
            add_to_queryset(queryset_params, 'is_wf_admin', False)

        if queryset_params:
            return MemberUser.objects.filter(**queryset_params)
        return MemberUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if member_user.id == request.data.get('created_by') or user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if member_user == instance.created_by or user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()


class UserToMemberAPI(viewsets.ModelViewSet):
    serializer_class = UserToMemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        member_id = self.request.query_params.get('member_id')  # int
        member_user_id = self.request.query_params.get('member_user_id')  # int
        is_owner = self.request.query_params.get('is_owner')  # bool

        queryset_params = {}
        add_to_queryset(queryset_params, 'member_id', member_id)
        add_to_queryset(queryset_params, 'member_user_id', member_user_id)

        if (is_owner == "true"):
            add_to_queryset(queryset_params, 'is_owner', True)
        elif (is_owner == "false"):
            add_to_queryset(queryset_params, 'is_owner', False)

        if queryset_params:
            return UserToMember.objects.filter(**queryset_params)
        return UserToMember.objects.all()


class PermissionsAPI(viewsets.ModelViewSet):
    serializer_class = PermissionsSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        can_add_calender_events = self.request.query_params.get('can_add_calender_events')  # bool
        can_add_employees = self.request.query_params.get('can_add_employees')  # bool
        can_delete_posts = self.request.query_params.get('can_delete_posts')  # bool
        can_edit_company_profile = self.request.query_params.get('can_edit_company_profile')  # bool
        can_edit_own_profile = self.request.query_params.get('can_edit_own_profile')  # bool
        is_member_admin = self.request.query_params.get('is_member_admin')  # bool
        role_title = self.request.query_params.get('role_title')
        member_id = self.request.query_params.get('member_id')  # int
        can_add_skills = self.request.query_params.get('can_add_skills')  # bool

        queryset_params = {}
        add_to_queryset(queryset_params, 'role_title__icontains', role_title)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if (can_add_calender_events == "true"):
            add_to_queryset(queryset_params, 'can_add_calender_events', True)
        elif (can_add_calender_events == "false"):
            add_to_queryset(queryset_params, 'can_add_calender_events', False)

        if (can_add_employees == "true"):
            add_to_queryset(queryset_params, 'can_add_employees', True)
        elif (can_add_employees == "false"):
            add_to_queryset(queryset_params, 'can_add_employees', False)

        if (can_delete_posts == "true"):
            add_to_queryset(queryset_params, 'can_delete_posts', True)
        elif (can_delete_posts == "false"):
            add_to_queryset(queryset_params, 'can_delete_posts', False)

        if (can_edit_company_profile == "true"):
            add_to_queryset(queryset_params, 'can_edit_company_profile', True)
        elif (can_edit_company_profile == "false"):
            add_to_queryset(queryset_params, 'can_edit_company_profile', False)

        if (can_edit_own_profile == "true"):
            add_to_queryset(queryset_params, 'can_edit_own_profile', True)
        elif (can_edit_own_profile == "false"):
            add_to_queryset(queryset_params, 'can_edit_own_profile', False)

        if (is_member_admin == "true"):
            add_to_queryset(queryset_params, 'is_member_admin', True)
        elif (is_member_admin == "false"):
            add_to_queryset(queryset_params, 'is_member_admin', False)

        if (can_add_skills == "true"):
            add_to_queryset(queryset_params, 'can_add_skills', True)
        elif (can_add_skills == "false"):
            add_to_queryset(queryset_params, 'can_add_skills', False)

        if queryset_params:
            return Permissions.objects.filter(**queryset_params)
        return Permissions.objects.all()


class UserRoleAPI(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        permissions_id = self.request.query_params.get('permissions_id')  # int
        user_id = self.request.query_params.get('user_id')  # int
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'permissions_id', permissions_id)
        add_to_queryset(queryset_params, 'user_id', user_id)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if queryset_params:
            return UserRole.objects.filter(**queryset_params)
        return UserRole.objects.all()


class GalleryAPI(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        image = self.request.query_params.get('image')
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'image__icontains', image)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if queryset_params:
            return Gallery.objects.filter(**queryset_params)
        return Gallery.objects.all()


class ApplicationAPI(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        org_name = self.request.query_params.get('org_name')
        org_email = self.request.query_params.get('org_email')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'email__icontains', email)
        add_to_queryset(queryset_params, 'org_name__icontains', org_name)
        add_to_queryset(queryset_params, 'org_email__icontains', org_email)

        if queryset_params:
            return Application.objects.filter(**queryset_params)
        return Application.objects.all()
