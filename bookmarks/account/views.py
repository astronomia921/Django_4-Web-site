from django.http import HttpResponse,  JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from actions.utils import create_action
from actions.models import Action

from .forms import (
    LoginForm, UserRegistrationForm,
    UserEditForm, ProfileEditForm)
from .models import Contact, Profile


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def user_list(request):
    template = 'account/user/list.html'
    users = User.objects.filter(is_active=True)
    context = {
        'section': 'people',
        'users': users
        }
    return render(request, template, context)


@login_required
def user_detail(request, username):
    template = 'account/user/detail.html'
    user = get_object_or_404(
        User, username=username, is_active=True
    )
    context = {
        'section': 'people',
        'user': user
    }
    return render(request, template, context)


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
            create_action(new_user, 'has created an account')
            return render(request, template_1, {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, template_2, {'user_form': user_form})


@login_required
def dashboard(request):
    template = 'account/dashboard.html'
    actions = Action.objects.exclude(
        user=request.user)
    following_ids = request.user.following.values_list(
        'id',
        flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = (actions
                   .select_related('user', 'user__profile')[:10]
                   .prefetch_related('target'))[:10]

    context = {'section': 'dashboard', 'actions': actions}
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
