from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from chatting.models import Message
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
    }
    return render(request, 'chatting/inbox.html', context)


@login_required
def chats(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages,
    }
    return render(request, 'chatting/chats.html', context)


@login_required
def send_chat(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')
    else:
        pass


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render


@login_required
def user_search(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(username__icontains=query)

        # Pagination
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        # when passing contexts, what's inside the ' ' will be called in the HTML template i.e. {{ profile.user }}
        context = {
            'users': users_paginator
        }

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # Check if the request is AJAX
        search_results = render_to_string('search_results.html', context)
        return HttpResponse(search_results, content_type='text/html')

    return render(request, 'search.html', context)


@login_required
# Sending a message to user from their profile button
def new_message(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('user_search')
    # if user sending message is not him/herself
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('inbox')
