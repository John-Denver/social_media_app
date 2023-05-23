from django.urls import path
from post import views


# the views.whatever whatever is the name of the function passed in views.py
# and the path specified on the first apostrophe(' ') will be on the browser search bar, i.e 127.0.0.1/8000/newpost
# and the name=IDK, IDK is used in the html file to call this url which references the views which references the models
from post.views import like_post

urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.new_post, name="new_post"),
    path('<uuid:post_id>/', views.post_detail, name="post_detail"),
    # path('tag/<slug:tag_slug>/', views.tags, name="hashtag"),

    path('tags/', views.tag_list, name='tag-list'),
    path('tags/<slug:slug>/', views.tag_detail, name='tag-detail'),

    # path('<uuid:post_id>/like', views.likes, name="like"),
    path('like-post/', views.like_post, name='like_post'),
    path('<uuid:post_id>/favourite', views.favourite, name="post-favourite"),

    path('story_detail/', views.story_detail, name='story_detail'),

]
