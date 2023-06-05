from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import resolve, reverse
from django.db import transaction

from comment.forms import CommentForm
from comment.models import Comment
from post.models import Post, Follow, Stream
from userauth.forms import *
from userauth.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    # Tracking profile stats (posts count, follow count, following count)
    post_count = Post.objects.filter(user=user).count()

    # People that are following me (coming from posts.model)
    followers_count = Follow.objects.filter(follower=user).count()
    following_count = Follow.objects.filter(following=user).count()  # People that I'm following

    # follow status .....to check whether you are following or not following a user
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    #  Pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    # when passing contexts what's inside the ' ' will be called in html templated i.e. {{ profile.user }}

    post_stream = Stream.objects.filter(user=user)
    group_ids = [post.post_id for post in post_stream]
    post_items = Post.objects.filter(id__in=group_ids).order_by('-posted')

    # Retrieve comments and select related users for each post
    comments = Comment.objects.filter(post_id__in=group_ids).select_related('user').order_by('-date')

    # Create a dictionary to map post IDs to their comments
    post_comments = {}
    for comment in comments:
        if comment.post_id not in post_comments:
            post_comments[comment.post_id] = []
        post_comments[comment.post_id].append(comment)

    # Count the comments for each post
    comment_counts = {post_id: len(comment_list) for post_id, comment_list in post_comments.items()}

    # Create a comment form instance
    comment_form = CommentForm()

    # Handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            # Get the post associated with the comment
            post_id = request.POST.get('post_id')  # Assuming you have a hidden input field with the post_id in the form
            post = Post.objects.get(id=post_id)
            # Create a new comment
            comment = Comment.objects.create(post=post, user=request.user, body=body)
            # Redirect back to the index page
            return redirect('index')

    context = {
        'posts_paginator': posts_paginator,
        'profile': profile,
        'posts': posts,
        'url_name': url_name,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'follow_status': follow_status,
        'comment_form': comment_form,
        'comment_counts': comment_counts,
    }
    return render(request, 'profile.html', context)


# The option is going to help track if a user is following a user or not
@login_required()
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            f.delete()
            # when unfollowed, the line below deletes the unfollowed users posts from the feed
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            # when followed, the line below list the posts of followed user and limits the stream to at least 10...
            # ...single user posts
            posts = Post.objects.filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required()
def edit_profile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.created = form.cleaned_data.get('created')
            profile.bio = form.cleaned_data.get('bio')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm
        context = {
            'form': form,
        }
        return render(request, 'edit-profile.html', context)


@login_required()
def add_profile(request):
    if request.method == "POST":
        form = AddProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello {username} your profile has been created successfully')
            return redirect('profile', profile.user.username)
    else:
        form = AddProfileForm()
    return render(request, 'add_profile.html', {'form': form})
