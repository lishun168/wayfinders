"""wayfinders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.core.exceptions import ViewDoesNotExist
from rest_framework import routers

from cal.api import CalendarAPI, FilterAPI
from events.api import EventAPI, InvitationAPI, ParticipantsAPI, GuestParticipantAPI
from forum.api import DiscussionAPI, PostAPI, ReplyAPI, MemberLikeOrFlagPostAPI, MemberLikeOrFlagReplyAPI
from groups.api import GroupsAPI, RulesAPI, GroupToMemberAPI
from search.api import SearchObjectAPI, SearchTagsAPI
from . import settings
from django.urls import path
from django.urls import include
from login.views import LoginPage
from login import views as login_views
from events import views as event_views
from forum import views as forums_views
from members import views as members_views

from members.views import CreateMemberProfile
from members.views import UpdatePassword
from members.views import CreateMemberChoice
from members.views import Index
from members.views import UserProfile
from members.views import MemberView
from members.views import EditMember
from members.views import EditMembersList
from members.views import MembersDirectory
from members.views import DirectorySearch
from members.views import MyProfile
from members.views import EditUser
from members.views import PermissionsView
from members.views import CreatePermissions
from members.views import EditPermissions
from members.views import Roles
from members.views import AssignRoles
from members.views import UpdateRoles
from members.views import RolesEditAll
from members.views import Invites
from members.views import SignUp
from members.views import CreateUser
from members.views import Approval
from members.views import UpdatePassword
from members.views import Application
from members.views import ApplicationSubmission
from members.views import ApplicationChoice
from members.views import ApplicationView
from members.views import ApplicationDetails
from members.views import ViewApplications
from members.views import ViewApplicationUploads
from members.views import ApplicationFileDetails
from members.views import ApplicationFileSubmit
from members.views import ApplicationSubmit
from members.views import ViewFlaggedUsers
from members.views import ViewFlaggedMembers
from skills.views import AddMemberSkill
from skills.views import CreateSkill
from skills.views import MemberSkill
from skills.views import ViewSkill
from skills.views import MySkills
from skills.views import AddSkill
from skills.views import UploadSkills
from skills.views import RemoveSkillFromMember
from skills.views import RemoveSkillFromUser
from industries.views import ViewIndustry
from industries.views import AddIndustry
from industries.views import AddMemberIndustry
from industries.views import MyIndustries
from industries.views import MemberIndustries
from industries.views import UploadIndustries
from industries.views import RemoveIndustryFromMember
from industries.views import RemoveIndustryFromUser
from groups.views import CreateGroup
from groups.views import EditGroup
from groups.views import LeaveGroup
from groups.views import MyGroups
from forum.views import ForumDirectory, flag_discussion
from forum.views import ThreadPage
from forum.views import CreateDiscussion
from forum.views import UpdateDiscussion
from forum.views import CreatePost
from forum.views import UpdatePost
from forum.views import CreateReply
from forum.views import UpdateReply
from forum.views import ViewFlaggedDiscussions
from forum.views import ViewFlaggedPosts
from forum.views import ViewFlaggedReplies
from cal.views import Calendar
from cal.views import CreateFilter
from cal.views import MyCalendar
from cal.views import CalendarDate
from cal.views import EditFilter
from events.views import CreateInvitation
from events.views import Invite
from events.views import CreateEvent
from events.views import UpdateEvent
from events.views import ViewEvent
from events.views import CreateBooking
from events.views import BookEvent
from events.views import MarkBusy
from events.views import CreateParticipant
from events.views import RemoveParticipant
from search.views import Search

from members.api import MemberAPI
from members.api import UserToMemberAPI
from members.api import PermissionsAPI
from members.api import UserRoleAPI
from members.api import GalleryAPI
from members.api import ApplicationAPI
from members.api import MemberUserAPI
from skills.api import SkillAPI
from skills.api import MemberToSkillsAPI
from skills.api import UserToSkillsAPI
from industries.api import IndustryAPI
from industries.api import MemberToIndustryAPI
from industries.api import UsertoIndustryAPI
from search.api import SearchObjectAPI
from search.api import SearchTagsAPI
from groups.api import GroupsAPI
from groups.api import RulesAPI
from groups.api import GroupToMemberAPI
from forum.api import DiscussionAPI
from forum.api import PostAPI
from forum.api import ReplyAPI
from forum.api import MemberLikeOrFlagPostAPI
from forum.api import MemberLikeOrFlagReplyAPI
from events.api import EventAPI
from events.api import InvitationAPI
from events.api import ParticipantsAPI
from events.api import GuestParticipantAPI
from cal.api import CalendarAPI
from cal.api import FilterAPI

## API ##
router = routers.DefaultRouter()
# From Member application(7)
router.register('api/members', MemberAPI, 'api/members')
router.register('api/member_users', MemberUserAPI, 'api/member_users')
router.register('api/users_members', UserToMemberAPI, 'api/users_members')
router.register('api/permissions', PermissionsAPI, 'api/permissions')
router.register('api/user_role', UserRoleAPI, 'api/member_users')
router.register('api/gallery', GalleryAPI, 'api/gallery')
router.register('api/application', ApplicationAPI, 'api/application')
# From Skills application(3)
router.register('api/skills', SkillAPI, 'api/skills')
router.register('api/member_skills', MemberToSkillsAPI, 'api/member_skills')
router.register('api/user_skills', UserToSkillsAPI, 'user_skills')
# From Search application(2)
router.register('api/search_object', SearchObjectAPI, 'api/search_object')
router.register('api/search_tags', SearchTagsAPI, 'api/search_tags')
# From Industries application(3)
router.register('api/industry', IndustryAPI, 'api/industry')
router.register('api/member_industry', MemberToIndustryAPI, 'api/member_industry')
router.register('api/user_industry', UsertoIndustryAPI, 'api/user_industry')
# From Groups application(3)
router.register('api/groups', GroupsAPI, 'api/groups')
router.register('api/rules', RulesAPI, 'api/rules')
router.register('api/group_member', GroupToMemberAPI, 'api/group_member')
# From Forum application(5)
router.register('api/discussion', DiscussionAPI, 'api/discussion')
router.register('api/post', PostAPI, 'api/post')
router.register('api/reply', ReplyAPI, 'api/reply')
router.register('api/member_like_or_flag_post', MemberLikeOrFlagPostAPI, 'api/member_like_or_flag_post')
router.register('api/member_like_or_flag_reply', MemberLikeOrFlagReplyAPI, 'api/member_like_or_flag_reply')
# From Event application(4)
router.register('api/event', EventAPI, 'api/event')
router.register('api/invitation', InvitationAPI, 'api/invitation')
router.register('api/participants', ParticipantsAPI, 'api/participants')
router.register('api/guest_participant', GuestParticipantAPI, 'api/guest_participant')
# From Cal application(8)
router.register('api/calendar', CalendarAPI, 'api/calendar')
router.register('api/filter', FilterAPI, 'api/filter')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view()),

    ## MEMBERS APP ##
    path('profile/<int:pk>/', UserProfile.as_view()),
    path('my_profile/', MyProfile.as_view()),
    path('edit_profile/<int:pk>', EditUser.as_view()),
    path('change_password/', UpdatePassword.as_view()),

    path('members/', MembersDirectory.as_view()),
    path('member/<int:pk>', MemberView.as_view()),
    path('pending_approval', Approval.as_view()),
    path('create_member/', CreateMemberProfile.as_view()),
    path('create_member_choice/', CreateMemberChoice.as_view()),
    path('edit_member/<int:pk>', EditMember.as_view()),
    path('edit_member_list/<int:pk>', EditMembersList.as_view()),

    path('permissions/<int:pk>', PermissionsView.as_view()),
    path('create_permissions/<int:member_pk>/', CreatePermissions.as_view()),
    path('edit_permissions/<int:pk>/<int:member_pk>/', EditPermissions.as_view()),

    path('roles/<int:pk>', Roles.as_view()),
    path('create_role/<int:member_pk>', AssignRoles.as_view()),
    path('edit_role/<int:pk>/<int:member_pk>/', UpdateRoles.as_view()),
    path('edit_all_roles/<int:pk>/', RolesEditAll.as_view()),

    path('flag_member/<int:member_pk>/<int:flagged_member_pk>', members_views.flag_member, name='flag_member'),
    path('flag_user/<int:member_pk>/<int:flagged_member_pk>', members_views.flag_user, name='flag_user'),
    path('view_flagged_users', ViewFlaggedUsers.as_view()),
    path('view_flagged_members', ViewFlaggedMembers.as_view()),
    # Update Many

    path('application/', Application.as_view()),
    path('submission/', ApplicationSubmission.as_view()),
    path('application_choice/', ApplicationChoice.as_view()),
    path('application_directory', ApplicationView.as_view()),
    path('application_files', ViewApplicationUploads.as_view()),
    path('application/<int:pk>/', ApplicationDetails.as_view()),
    path('applications/', ViewApplications.as_view()),
    path('application_file/<int:pk>', ApplicationFileDetails.as_view()),
    path('process_application/<int:pk>/<str:approved>', ApplicationSubmit.as_view()),
    path('process_file_application/<int:pk>/<str:approved>', ApplicationFileSubmit.as_view()),

    ## LOGIN APP ##
    path('login_page', LoginPage.as_view()),
    path('login/', login_views.login_view),
    path('logout/', login_views.logout_view),
    path('signup/<int:pk>', SignUp.as_view()),

    ## FORUM APP ##
    path('forum', ForumDirectory.as_view()),
    path('forum/<int:pk>', ThreadPage.as_view()),
    path('forum/create', CreateDiscussion.as_view()),
    path('forum/update/<int:pk>', UpdateDiscussion.as_view()),
    path('forum/post/<int:pk>', CreatePost.as_view()),
    path('forum/post/update/<int:pk>', UpdatePost.as_view()),
    path('forum/reply/<int:pk>/<int:post_pk>', CreateReply.as_view()),
    path('forum/reply/update/<int:pk>', UpdateReply.as_view()),
    path('like/<int:member_pk>/<int:post_pk>', forums_views.like, name='like'),
    path('flag/<int:member_pk>/<int:post_pk>', forums_views.flag, name='flag'),
    path('flag_discussion/<int:member_pk>/<int:discussion_pk>', forums_views.flag_discussion, name='flag_discussion'),
    path('sticky/<int:discussion_pk>', forums_views.sticky),
    path('view_flagged_discussions', ViewFlaggedDiscussions.as_view()),
    path('view_flagged_posts', ViewFlaggedPosts.as_view()),
    path('view_flagged_replies', ViewFlaggedReplies.as_view()),

    ## CALENDAR APP ##
    path('calendar/<int:pk>', Calendar.as_view()),
    path('calendar/<int:pk>/<int:year>/<int:month>', CalendarDate.as_view()),
    path('create_filter/<int:pk>', CreateFilter.as_view()),
    path('my_calendar/', MyCalendar.as_view()),
    path('edit_filter/<int:pk>', EditFilter.as_view()),

    ## EVENT APP ##
    path('edit_event/<int:pk>', UpdateEvent.as_view()),
    path('create_event/<int:pk>', CreateEvent.as_view()),
    path('create_booking/<int:pk>', CreateBooking.as_view()),
    path('mark_busy/<int:pk>', MarkBusy.as_view()),
    path('book_event/<int:pk>/<int:cal_pk>', BookEvent.as_view()),
    path('event/<int:pk>', ViewEvent.as_view()),
    path('invite/<int:pk>', CreateInvitation.as_view()),
    path('accept_invite/<int:invite_pk>', event_views.accept_view),
    path('decline_invite/<int:invite_pk>', event_views.decline_view),
    path('join_event/<int:event_pk>/<int:user_pk>', event_views.join_view),
    path('invites/<int:pk>', Invites.as_view()),
    path('get_invite/<int:pk>', Invite.as_view()),
    path('add_participant/<int:pk>', CreateParticipant.as_view()),
    path('remove_participant/<int:pk>/<int:event_pk>', RemoveParticipant.as_view()),

    ## GROUP APP 
    path('create_group/<int:pk>', CreateGroup.as_view()),
    path('edit_group/<int:pk>', EditGroup.as_view()),
    path('my_groups/<int:pk>', MyGroups.as_view()),
    path('leave_group/<int:pk>', LeaveGroup.as_view()),

    ## SKILL APP ##
    path('create_skill/<int:pk>', CreateSkill.as_view()),
    path('my_skills/<int:pk>', MySkills.as_view()),
    path('skill/<int:pk>', ViewSkill.as_view()),
    path('add_skill/<int:pk>', AddSkill.as_view()),
    path('member_skills/<int:pk>', MemberSkill.as_view()),
    path('add_member_skill/<int:pk>', AddMemberSkill.as_view()),
    path('upload_skills/', UploadSkills.as_view()),
    path('remove_skill_user/<int:pk>/<int:user_pk>', RemoveSkillFromUser.as_view()),
    path('remove_skill_member/<int:pk>/<int:member_pk>', RemoveSkillFromMember.as_view()),

    ## INDUSTRY APP ##
    path('industry/<int:pk>', ViewIndustry.as_view()),
    path('add_member_industry/<int:pk>', AddMemberIndustry.as_view()),
    path('add_industry/<int:pk>', AddIndustry.as_view()),
    path('member_industries/<int:pk>', MemberIndustries.as_view()),
    path('my_industries/<int:pk>', MyIndustries.as_view()),
    path('upload_industries/', UploadIndustries.as_view()),
    path('remove_industry_user/<int:pk>/<int:user_pk>', RemoveIndustryFromUser.as_view()),
    path('remove_industry_member/<int:pk>/<int:member_pk>', RemoveIndustryFromMember.as_view()),

    ## SEARCH APP ##
    path('global_search/<str:query>', Search.as_view()),
    path('search/<str:query>', DirectorySearch.as_view()),

    path('api/', include(router.urls))
]


urlpatterns += router.urls
urlpatterns += path('auth/', include('knox.urls')),
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
