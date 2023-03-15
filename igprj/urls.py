"""igprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from userauth.models import Profile
from userauth.views import *

from comment.models import *
from comment.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('users/', include('userauth.urls')),
    # path('comment/', include('comment.urls')),

    #     Profile page urls

    # in userauth views.py the fct user_profile has an if statement that says if url_name == 'profile': ...
    # so in the path name we are passing the "name" profile to reference that

    # also in the path direction we are passing '<username>/' so that...
    # if a user just rights the username in front of the url ...
    # i.e 127.0.0.1/8000/username he can go to the usernames profile page
    path('<username>/', user_profile, name="profile"),
    path('<username>/saved', user_profile, name="favourite"),
    path('<username>/follow/<option>', follow, name="follow"),

    # path('<username>/edit_profile', edit_profile, name="edit_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
