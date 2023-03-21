from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chatting.models import Message


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
