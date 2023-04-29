from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from.forms import UserRegisterForm


def home(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello {username} your account has been created successfully add profile')

            # automatically log in user
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('edit_profile')
    #     the view add_profile above is from userauth app
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
