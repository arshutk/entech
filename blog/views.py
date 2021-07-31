import json
from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Vote, Comment
from .forms import (PostForm, CommentForm)

@login_required
def post_create_view(request):
    context = {}

    # POST request
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.written_by = request.user
            obj.save()
            messages.success(request, 'Post created successfully')
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'blog/post_create.html', context)
    
    # GET request
    else:
        form = PostForm()
        context['form'] = form
    
    return render(request, 'blog/post_create.html', context)

@login_required
def comment_like_delete_view(request, post_slug, comment_id=None):
    post = get_object_or_404(Post, slug=post_slug)
    
    action = request.GET.get('action')

    user = request .user

    try:
        comment = Comment.objects.get(id = comment_id)
    except:
        comment = None

    # POST request
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.written_by = user     
            
            obj.comment = comment 
            obj.save()
            return redirect('post_detail', post_slug=post.slug)
        else:
            return HttpResponse(json.dumps({'detail': form.errors}), content_type="application/json")

    # deleting comment / making it inactive
    elif action == 'delete' and comment and comment.written_by == request.user:
        comment.status = Comment.STATUS.INACTIVE
        comment.save()

    # adding like to comment
    elif user not in comment.liked_by.all() and (action == 'like'):
            comment.liked_by.add(user)

    # removing like from comment
    elif user in comment.liked_by.all() and (action == 'unlike'):
        comment.liked_by.remove(user)

    return redirect('post_detail', post_slug=post.slug)


def home_view(request):
    posts = Post.objects.all().exclude(status=Post.STATUS.INACTIVE)
    # posts = Post.objects.all().exclude(written_by = request.user)
    
    if request.user.is_authenticated:
        action = request.GET.get('action')
        if action == 'bookmarked':
            posts = Post.objects.filter(bookmarked_by=request.user).exclude(status=Post.STATUS.INACTIVE)
        elif action == 'created':
            posts = Post.objects.filter(written_by=request.user).exclude(status=Post.STATUS.INACTIVE)
    print(messages)
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail_view(request, post_slug):
    user  = request.user

    try:
        post = Post.objects.get(slug=post_slug)
    except:
        raise Http404

    try:
        vote = post.reactions.get(voter=user)
    except:
        vote = None

    try:
        comments = post.comments.all().exclude(status=Comment.STATUS.INACTIVE).prefetch_related('liked_by')
    except:
        comments = None

    context = {
        'post': post, 
        'meta': post.as_meta(),
        'bookmark_status': True if request.user in post.bookmarked_by.all() else False, 
        'reaction': vote.vote_type if vote else None,
        'comments': comments,
    }

    action = request.GET.get('action')

    if action in ['add', 'remove']:
        if user.is_authenticated:
            # Post bookmarked
            if user not in post.bookmarked_by.all() and (action == 'add'):
                post.bookmarked_by.add(request.user)
                context['detail'] = 'Post Bookmarked'
                context['bookmark_status'] = True

            # Bookmark removed
            elif user in post.bookmarked_by.all() and (action == 'remove'):
                post.bookmarked_by.remove(request.user)
                context['detail'] = 'Bookmarked removed'
                context['bookmark_status'] = False
        else:
            return redirect('login')
    
    elif action in ['like', 'love', 'insightful']:
        if user.is_authenticated:
            # Add reaction to post
            vote_type = action
            if vote:
                if vote.vote_type == vote_type:
                    # If reaction already exists
                    pass
                else:
                    # If reaction exists but user wants to change the reaction
                    vote.vote_type = vote_type   
                    vote.save()
                    context['reaction'] = vote_type
            else:
                # If no previous reaction on the post exists
                Vote.objects.create(post=post, voter=user, vote_type=vote_type)
                context['reaction'] = vote_type
        else:
            return redirect('login')
                    
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit_delete_view(request, post_slug):
    post = get_object_or_404(Post, slug = post_slug)
    action = request.GET.get('action')

    if action in ['edit', 'delete'] and post.written_by == request.user:
        if action == 'edit':
            return redirect('post_edit', post_slug=post.slug)
        else:
            post.status = post.STATUS.INACTIVE
            post.save()
            return redirect('home')

    return redirect('home')

@login_required
def post_edit_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {}

    # POST request
    if request.POST:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.written_by = request.user
            obj.save()
            messages.success(request, 'Post updated successfully')
            return redirect('post_detail', post_slug=obj.slug)
        else:
            context['form'] = form
            return render(request, 'blog/post_edit.html', context)
    
    # GET request
    else:
        form = PostForm(instance=post)
        context['form'] = form
    
    return render(request, 'blog/post_edit.html', context)


def test_view(request):
    return HttpResponse('<h1>Yeah seems alright</h1>')