from django.urls import path

from stories import views

urlpatterns = [
    path('newstory/', views.new_story, name='newstory'),
    path('showmedia/<stream_id>', views.show_media, name='showmedia'),
]
