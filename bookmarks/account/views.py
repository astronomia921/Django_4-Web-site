from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import (
    LoginForm, UserRegistrationForm,
    UserEditForm, ProfileEditForm)
from .models import Profile


def register(request):
    template_1 = 'account/register_done.html'
    template_2 = 'account/register.html'
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, template_1, {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, template_2, {'user_form': user_form})


@login_required
def dashboard(request):
    template = 'account/dashboard.html'
    context = {'section': 'dashboard'}
    return render(request, template, context)


@login_required
def edit(request):
    template = 'account/edit.html'
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, template, context)


def user_login(request):
    template = 'account/login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, template, context)
