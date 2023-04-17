from django.urls import path
from userauth import views


# the views.whatever whatever is the name of the function passed in views.py
# and the path specified on the first apostrophe(' ') will be on the browser search bar, i.e 127.0.0.1/8000/newpost
# and the name=IDK, IDK is used in the html file to call this url which references the views which references the models
from userauth.views import user_profile

urlpatterns = [
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('add_profile/', views.add_profile, name="add_profile"),
]
