from django.urls import path
from . import views
from members.views import Index, Member, Company, MembersDirectory, DirectorySearch, LoginPage, MyProfile, EditMember, CreateMember
from members import views as member_views

urlpatterns = [
    
]