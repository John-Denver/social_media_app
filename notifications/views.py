from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification


def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
    Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)

    template = loader.get_template('notifications/notification.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))


def delete_notification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, recipient=user).delete()
    return redirect('show-notifications')


def count_notification(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()

    return {'count_notifications': count_notifications}
