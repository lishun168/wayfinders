from django.contrib import admin
from .models import MemberToSkills, Skill, UserToSkills

admin.site.register(Skill)
admin.site.register(MemberToSkills)
admin.site.register(UserToSkills)

