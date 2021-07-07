from django.contrib import admin

from .models import Discussion, Post, Reply

admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Reply)

# Register your models here.
