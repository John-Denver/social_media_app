from django.shortcuts import render, redirect, get_object_or_404

from comment.forms import CommentForm
from post.models import Tag, Post, Stream, Follow, Likes
from django.contrib.auth.decorators import login_required
from post.forms import NewPostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from userauth.models import Profile
from comment.models import Comment


# Create your views here.

# the redirect if not logged in has been specified in settings.py under LOGIN_URL
@login_required()
def index(request):
    user = request.user  # get logged in user
    posts = Stream.objects.filter(user=user)  # stream from models, this line gets posts of current logged-in user
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    # -posted gives results of the latest post at the top while posted the latest result is at the bottom
    # posted is a string but references posted in models.py
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items': post_items,
    }
    return render(request, 'index.html', context)

@login_required()
def new_post(request):
    user = request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list = list(tag_form.split(','))
            # when user puts a comma the above code will know that now it's a different hashtag being put

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tag.set(tags_objs)
            p.save()
            # return and execute the function named index
            return redirect('index')

        # if method in form is not POST

    else:
        form = NewPostForm()
        context = {
            'form': form
        }
        return render(request, 'newpost.html', context)

@login_required()
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # commenting on a post
    comments = Comment.objects.filter(post=post).order_by('-date')
    comment_count = Comment.objects.filter(post=post_id).count()

    # Comment Form
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            # return and execute the function named index
            return HttpResponseRedirect(reverse("post_detail", args=[post_id]))

    else:
        form = CommentForm()
        context = {
            'form': form,
            'post': post,
            'comments': comments,
            'comment_count': comment_count,
            }
        return render(request, 'post-detail.html', context)

@login_required()
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')

    context = {
        'tag': tag,
        'posts': posts
    }

    return render(request, 'hashtags.html', context)

@login_required()
def likes(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    # the post.likes above comes from models.py class Post which takes the variable likes
    # so like is associated to a post hence, post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))

@login_required()
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))
