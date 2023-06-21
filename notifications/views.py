from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from notifications.models import Notification
from post.models import Follow


@login_required
def show_notifications(request):
    user = request.user
    all_users = User.objects.all()

    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')

    # Get the unique sender usernames from the notifications
    sender_usernames = list(set(notification.sender.username for notification in notifications))

    # Get the follow status for each sender
    follow_status = {username: Follow.objects.filter(following__username=username, follower=user).exists() for
                     username in sender_usernames}

    # Get the current date and time
    now = timezone.now()

    # Calculate the start and end dates for "Today"
    today_start = now.date()
    today_end = today_start + timedelta(days=1)

    # Calculate the start and end dates for "This Week"
    this_week_start = today_start - timedelta(days=today_start.weekday())
    this_week_end = this_week_start + timedelta(days=7)

    # Filter notifications based on their timestamps
    today_notifications = notifications.filter(timestamp__range=(today_start, today_end))
    this_week_notifications = notifications.filter(timestamp__range=(this_week_start, this_week_end)).exclude(
        timestamp__range=(today_start, today_end))
    other_notifications = notifications.filter(timestamp__lt=this_week_start)

    # Update the 'is_read' status of the notifications
    notifications.filter(is_read=False).update(is_read=True)

    count_notifications = notifications.filter(is_read=False).count()

    template = loader.get_template('notifications/notification.html')

    context = {
        'all_users': all_users,
        'follow_status': follow_status,
        'today_notifications': today_notifications,
        'this_week_notifications': this_week_notifications,
        'other_notifications': other_notifications,
        'count_notifications': count_notifications,
    }

    return HttpResponse(template.render(context, request))


@login_required
def delete_notification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, recipient=user).delete()
    return redirect('show-notifications')


@login_required
def count_notification(request):
    user = request.user
    count_notifications = 0
    if user.is_authenticated:
        count_notifications = Notification.objects.filter(recipient=user, is_read=False).count()

    return JsonResponse({'count_notifications': count_notifications})

# @login_required
# def show_notifications(request):
#     user = request.user
#     notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
#     Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
#
#     count_notifications = 0
#     if user.is_authenticated:
#         count_notifications = Notification.objects.filter(recipient=user, is_read=False).count()
#
#     template = loader.get_template('notifications/notification.html')
#
#     context = {
#         'notifications': notifications,
#         'count_notifications': count_notifications,
#     }
#
#     return HttpResponse(template.render(context, request))
