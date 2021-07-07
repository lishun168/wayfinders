from django.contrib import admin
from .models import Industry, MemberToIndustry

admin.site.register(Industry)
admin.site.register(MemberToIndustry)
