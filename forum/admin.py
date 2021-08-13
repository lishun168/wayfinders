from django.contrib import admin

from .models import Discussion
from .models import Post
from .models import Reply
from .models import MemberLikeOrFlagReply
from .models import MemberLikeOrFlagPost
from .models import UserFlagPost

admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(MemberLikeOrFlagPost)
admin.site.register(MemberLikeOrFlagReply)
admin.site.register(UserFlagPost)

# Register your models here.
