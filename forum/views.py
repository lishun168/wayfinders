from django.shortcuts import render
from django.views import View
from .models import Discussion
from .models import Post
from .models import Reply
from .models import MemberLikeOrFlagPost
from .models import MemberLikeOrFlagReply
from .models import UserFlagPost
from members.models import MemberUser
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators import csrf
from django.core.paginator import Paginator
from login.views import LoginPermissionMixin
from django.core.exceptions import PermissionDenied
from wayfinders.functions import add_to_queryset
import operator
from django.contrib import messages
from django.db.models import Q
from .forms import SearchForm

import logging
logger = logging.getLogger(__name__)

class ForumDirectory(LoginPermissionMixin, View):
    template_name='forum/forum_directory.html'

    def get(self, request):
        form = SearchForm()
        context = {
            'form': form
        }
        oldest = request.GET.get("oldest")
        sticky = request.GET.get("sticky")
        subject = request.GET.get("subject")
        contains = request.GET.get("contains")
        check_flags = request.GET.get("check_flags")
        likes = request.GET.get("likes")

        queryQ = Q()
        if subject:
            queryQ &= Q(title__icontains=subject) | Q(subtitle__icontains=subject)
        if contains:
            queryQ &= Q(post__body__icontains=contains) | Q(reply__body__contains=contains)
               
        discussions = Discussion.objects.filter(queryQ)
        member_user = MemberUser.objects.get(user=self.request.user)
        member_flags = UserFlagPost.objects.filter(user=member_user)

        for discussion in discussions:
            for flag in member_flags:
                if flag.discussion == discussion and flag.flagged == True:
                    discussion.flagged = True

        if oldest == "true":
            discussions = sorted(discussions, key=operator.attrgetter('created_at'))
        else:
            discussions = sorted(discussions, key=operator.attrgetter('created_at'), reverse=True)

        if likes == "true":
            discussions = sorted(discussions, key=operator.attrgetter('likes'), reverse=True)
        if sticky != "false":
            discussions = sorted(discussions, key=operator.attrgetter('sticky'), reverse=True)
        if check_flags == "true":
            discussions = sorted(discussions, key=operator.attrgetter('number_of_flags'), reverse=True)
            context['check_flags'] = True

        context['threads'] = discussions
    
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            contains = form.cleaned_data['contains']
            likes = form.cleaned_data['likes']
            sticky = form.cleaned_data['sticky']

            logger.error("valid")
            logger.error(form)

            search_url = "/forum?"
            if subject:
                search_url += "subject=" + subject + "&"
            if contains:
                search_url += "contains=" + contains + "&"
            if likes:
                search_url += "likes=" + str(likes).lower() + "&"

            search_url += "sticky=" + str(sticky).lower() + "&"

            return HttpResponseRedirect(search_url)
                
        
        messages.add_message(request, messages.ERROR, "Search failed. Invalid Search")
        search_url = "/forum"
        return HttpResponseRedirect(search_url)

class ThreadPage(LoginPermissionMixin, View):
    template_name='forum/discussion.html'

    def get(self, request, pk):

        posts = Post.objects.filter(discussion=pk).order_by('-created_at')
        replies = Reply.objects.filter(discussion=pk).order_by('created_at')
        thread = Discussion.objects.get(pk=pk)

        user_member = MemberUser.objects.get(user=request.user.pk)
        like_or_flag_posts = MemberLikeOrFlagPost.objects.filter(member=user_member, post__discussion=thread)
        like_or_flag_replies = MemberLikeOrFlagReply.objects.filter(member=user_member, reply__discussion=thread)

        forum_admin = self.request.user.is_superuser or user_member.is_wf_admin or user_member.is_forum_mod

        for post in posts:
            for flag in like_or_flag_posts:
                if flag.post == post:
                    if flag.flagged == True:
                        post.flagged = True
                    else:
                        post.flagged = False
                    if flag.like == True:
                        post.liked = True
                    else:
                        post.liked = False

        for reply in replies:
            for flag in like_or_flag_posts:
                if reply.post == post:
                    if flag.flagged == True:
                        reply.flagged = True
                    else:
                        reply.flagged = False
                    if flag.like == True:
                        reply.liked = True
                    else:
                        reply.liked = False
                

        context = {
            'thread': thread,
            'posts': posts,
            'replies': replies,
            'user': user_member,
            'like_or_flag_posts': like_or_flag_posts,
            'like_or_flag_replies': like_or_flag_replies,
            'forum_admin': forum_admin
        }

        return render(request, self.template_name, context)

class CreateDiscussion(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Discussion
    fields = ('title', 'subtitle')
    
    def get_context_data(self, **kwargs):
        context = super(CreateDiscussion, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Discussion'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateDiscussion, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        member = MemberUser.objects.get(user=self.request.user)
        obj.created_by = member
        obj.created_by_string = member.first_name + member.last_name
        obj.save()

        success_url = '/forum/' + str(obj.pk)
        return HttpResponseRedirect(success_url)

class UpdateDiscussion(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Discussion
    fields = ('title', 'subtitle')

    def get_object(self, *args, **kwargs):
        obj = super(UpdateDiscussion, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            discussion = Discussion.objects.get(pk=self.kwargs.get('pk'))
           
            if member != discussion.created_by:
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(UpdateDiscussion, self).get_context_data(**kwargs)
        context['button_text'] = 'Update Discussion'
        return context

    def dispatch(self, *args, **kwargs):
        return super(UpdateDiscussion, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        success_url = '/forum/' + str(obj.pk)
        return HttpResponseRedirect(success_url)
   

class CreatePost(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Post
    fields = ('body',)

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Post'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreatePost, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        member = MemberUser.objects.get(user=self.request.user)
        obj.created_by = member
        obj.created_by_string = member.first_name + member.last_name
        discussion_pk = self.kwargs.get('pk')
      
        discussion = Discussion.objects.get(pk=discussion_pk)
        obj.discussion = discussion
        obj.save()
        success_url = '/forum/' + str(discussion_pk) 
        return HttpResponseRedirect(success_url)

class UpdatePost(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Post
    fields = ('body',)

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePost, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            post = Post.objects.get(pk=self.kwargs.get('pk'))
            if member != post.created_by:
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(UpdatePost, self).get_context_data(**kwargs)
        context['button_text'] = 'Update Post'
        return context

    def dispatch(self, *args, **kwargs):
        return super(UpdatePost, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        thread_pk = obj.discussion.pk
        obj.save()

        success_url = '/forum/' + str(thread_pk)
        return HttpResponseRedirect(success_url)
    

class CreateReply(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Reply
    fields = ('body',)

    def get_context_data(self, **kwargs):
        context = super(CreateReply, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Reply'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateReply, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        member = MemberUser.objects.get(user=self.request.user)
        obj.created_by = member
        obj.created_by_string = member.first_name + member.last_name

        thread_pk = self.kwargs.get('pk')
        thread = Discussion.objects.get(pk=thread_pk)
        obj.discussion = thread

        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        obj.post = post

        obj.save()
        success_url = '/forum/' + str(thread_pk)
        return HttpResponseRedirect(success_url)

class UpdateReply(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Reply
    fields = ('body',)

    def get_object(self, *args, **kwargs):
        obj = super(UpdateReply, self).get_object(*args, **kwargs)
        try:
            member = MemberUser.objects.get(user=self.request.user)
            reply = Reply.objects.get(pk=self.kwargs.get('pk'))
            if member != reply.created_by:
                raise PermissionDenied()
        except MemberUser.DoesNotExist:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs):
        context = super(UpdateReply, self).get_context_data(**kwargs)
        context['button_text'] = 'Update Reply'
        return context

    def dispatch(self, *args, **kwargs):
        return super(UpdateReply, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        thread_pk = obj.discussion.pk
        obj.save()

        success_url = '/forum/' + str(thread_pk)
        return HttpResponseRedirect(success_url)

class ViewFlaggedDiscussions(View):
    template_name = 'forum/flags.html'

    def get(self, request):
        discussions = Discussion.objects.filter(number_of_flags__gt=0).distinct().order_by('-number_of_flags')

        context = {
            'discussions': discussions
        }

        return render(request, self.template_name, context)

class ViewFlaggedPosts(View):
    template_name = 'forum/flags.html'

    def get(self, request):
        posts = Post.objects.filter(number_of_flags__gt=0).distinct().order_by('-number_of_flags')

        context = {
            'posts': posts
        }

        return render(request, self.template_name, context)

class ViewFlaggedReplies(View):
    template_name = 'forum/flags.html'

    def get(self, request):
        replies = Reply.objects.filter(number_of_flags__gt=0).distinct().order_by('-number_of_flags')

        context = {
            'replies': replies
        }

        return render(request, self.template_name, context)

@csrf.csrf_exempt
def sticky(request, discussion_pk):
    discussion = Discussion.objects.get(pk=discussion_pk)
    if discussion.sticky == True:
        discussion.sticky = False
    else:
        discussion.sticky = True
    discussion.save()
    success_url = '/forum'
    return HttpResponseRedirect(success_url)

@csrf.csrf_exempt
def like(request, member_pk, post_pk):
    member = MemberUser.objects.get(pk=member_pk)
    post = Post.objects.get(pk=post_pk)
    try:
        member_post = MemberLikeOrFlagPost.objects.get(member=member, post=post)
        if member_post.like is True:
            member_post.like = False
            post.likes -=1
        else:
            member_post.like = True
            post.likes += 1
        post.save()
        member_post.save()
    except MemberLikeOrFlagPost.DoesNotExist:
        member_post = MemberLikeOrFlagPost()
        member_post.like = True
        member_post.member = member
        member_post.post = post
        member_post.save()

        post.likes +=1
        post.save()

    success_url = "/forum/" + str(post.discussion.pk)
    return HttpResponseRedirect(success_url)

@csrf.csrf_exempt
def like_reply(request, member_pk, reply_pk):
    member = MemberUser.objects.get(pk=member_pk)
    reply = Reply.objects.get(pk=reply_pk)
    try:
        member_reply = MemberLikeOrFlagReply.objects.get(member=member, reply=reply)
        if member_reply.like is True:
            member_reply.like = False
            reply.likes -=1
        else:
            member_reply.like = True
            reply.likes += 1
        reply.save()
        member_reply.save()
    except MemberLikeOrFlagReply.DoesNotExist:
        member_reply = MemberLikeOrFlagReply()
        member_reply.like = True
        member_reply.member = member
        member_reply.reply = reply
        member_reply.save()

        reply.likes += 1
        reply.save()

    success_url = "/forum/" + str(reply.discussion.pk)
    return HttpResponseRedirect(success_url)

@csrf.csrf_exempt
def flag(request, member_pk, post_pk):
    post = Post.objects.get(pk=post_pk)
    member = MemberUser.objects.get(pk=member_pk)
    try:
        member_post = MemberLikeOrFlagPost.objects.get(member=member, post=post)
        if member_post.flagged is True:
            member_post.flagged = False
            post.number_of_flags -=1
        else:
            member_post.flagged = True
            post.number_of_flags += 1
            post.flagged = True
        post.save()
        member_post.save()
    except MemberLikeOrFlagPost.DoesNotExist:
        member_post = MemberLikeOrFlagPost()
        member_post.flagged = True
        member_post.member = member
        member_post.post = post
        member_post.save()

        post.flagged = True
        post.number_of_flags +=1
        post.save()

    success_url = "/forum/" + str(post.discussion.pk)
    return HttpResponseRedirect(success_url)

@csrf.csrf_exempt
def flag_reply(request, member_pk, reply_pk):
    reply = Reply.objects.get(pk=reply_pk)
    member = MemberUser.objects.get(pk=member_pk)
    try:
        member_reply = MemberLikeOrFlagReply.objects.get(member=member, reply=reply)
        if member_reply.flagged is True:
            member_reply.flagged = False
            reply.number_of_flags -=1
        else:
            member_reply.flagged = True
            reply.number_of_flags += 1
            reply.flagged = True
        reply.save()
        member_reply.save()
    except MemberLikeOrFlagPost.DoesNotExist:
        member_reply = MemberLikeOrFlagPost()
        member_reply.flagged = True
        member_reply.member = member
        member_reply.reply = reply
        member_reply.save()

        reply.flagged = True
        reply.number_of_flags +=1
        reply.save()

    success_url = "/forum/" + str(reply.discussion.pk)
    return HttpResponseRedirect(success_url)

@csrf.csrf_exempt
def flag_discussion(request, member_pk, discussion_pk):
    member = MemberUser.objects.get(pk=member_pk)
    discussion = Discussion.objects.get(pk=discussion_pk)
    try:
        user_flag_discussion = UserFlagPost.objects.get(user=member, discussion=discussion)
        if user_flag_discussion.flagged is True:
            user_flag_discussion.flagged = False
            discussion.number_of_flags -=1
        else:
            user_flag_discussion.flagged = True
            discussion.number_of_flags += 1
        discussion.save()
        user_flag_discussion.save()
    except UserFlagPost.DoesNotExist:
        user_flag_discussion = UserFlagPost()
        user_flag_discussion.flagged = True
        user_flag_discussion.user = member
        user_flag_discussion.discussion = discussion
        user_flag_discussion.save()

        discussion.number_of_flags += 1
        discussion.save()

    success_url = "/forum"
    return HttpResponseRedirect(success_url)

