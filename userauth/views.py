from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import resolve, reverse
from django.db import transaction


from post.models import Post, Follow, Stream
from userauth.models import *


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
    context = {
        'posts_paginator': posts_paginator,
        'profile': profile,
        'posts': posts,
        'url_name': url_name,
        'post_count': post_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'follow_status': follow_status,
    }
    return render(request, 'profile.html', context)


def user_urls(request, username):
    user_username = get_object_or_404(User, username=username)

    context = {
        'user_username': user_username,
    }
    return render(request, 'index.html', context)


# The option is going to help track if a user is following a user or not
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
                    stream = Stream(post=post, user=user, date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))
