from django.urls import path
from chatting import views


# the views.whatever whatever is the name of the function passed in views.py
# and the path specified on the first apostrophe(' ') will be on the browser search bar, i.e 127.0.0.1/8000/newpost
# and the name=IDK, IDK is used in the html file to call this url which references the views which references the models


urlpatterns = [
    path('inbox/', views.inbox, name="inbox"),

]
