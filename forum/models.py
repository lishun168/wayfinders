from django.db import models
from datetime import datetime
from members.models import MemberUser


class Discussion(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(MemberUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_string = models.CharField(max_length=255)
    sticky = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    number_of_flags = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name='Discussion'
        verbose_name_plural='Discussions'

class Post(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(MemberUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_string = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    flagged = models.BooleanField(default=False)
    number_of_flags = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.discussion, self.created_at )

class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(MemberUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_string = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    flagged = models.BooleanField(default=False)
    number_of_flags = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.discussion, self.created_at )

    class Meta:
        verbose_name='Reply'
        verbose_name_plural='Replies'

class MemberLikeOrFlagPost(models.Model):
    member = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    like = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.member, self.post)

    class Meta:
        verbose_name='Member Likes Post'
        verbose_name_plural='Members Like Posts'

class MemberLikeOrFlagReply(models.Model):
    member = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    like = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.member, self.reply)

    class Meta:
        verbose_name='Member Likes Reply'
        verbose_name_plural='Members Like Replies'






    #like or flag async
    #filtering like and dislike





