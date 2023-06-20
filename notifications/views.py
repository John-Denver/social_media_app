from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse

from notifications.models import Notification


@login_required
def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
    Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)

    count_notifications = 0
    if user.is_authenticated:
        count_notifications = Notification.objects.filter(recipient=user, is_read=False).count()

    template = loader.get_template('notifications/notification.html')

    context = {
        'notifications': notifications,
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
