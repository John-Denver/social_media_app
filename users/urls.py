from django.urls import path
from users import views

# below code is for the django login and logout view pre-made
from django.contrib.auth import views as auth_view


# the views.whatever whatever is the name of the function passed in views.py
# and the path specified on the first apostrophe(' ') will be on the browser search bar, i.e 127.0.0.1/8000/newpost
# and the name=IDK, IDK is used in the html file to call this url which references the views which references the models


urlpatterns = [
    # The login and logout view has been pre-made by django no need for the views.py
    # in settings.py specify your redirect
    path('auth/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('auth/logout', auth_view.LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),

]
