from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomLoginForm


def register_or_login(request, template_name='register_or_login.html'):
    register_form = CustomUserCreationForm()
    login_form = CustomLoginForm()

    active_form = "register"  

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()  
                active_form = "login"  

        elif 'login' in request.POST:
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')

                user = authenticate(
                    request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('main:index')
                else:
                    login_form.add_error(
                        None, "نام کاربری یا رمز عبور اشتباه است.")
            active_form = "login"

    return render(request, template_name, {
        'register_form': register_form,
        'login_form': login_form,
        'active_form': active_form 
    })
