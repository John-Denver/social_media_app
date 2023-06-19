from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.show_notifications, name='show-notifications'),
    path('<noti_id>/delete', views.delete_notification, name='delete-notification'),
    ]
