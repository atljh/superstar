from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from apps.home.models import Modul
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.is_online = False
    user.save()


def is_moderator(user):
    return user.groups.filter(name='Moderator').exists()

def is_administrator(user):
    return user.groups.filter(name='Administrator').exists()

def is_moderator(user):
    return user.groups.filter(name='Client').exists()


@login_required(login_url="/login/")
def users_observe(request):
    users = User.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'users/users-observe.html', context=context)


@login_required(login_url="/login/")
def users_control(request):
    groups = Group.objects.all()
    moduls = Modul.objects.all()

    context = {
        'groups': groups,
        'moduls': moduls

    }
    return render(request, 'users/users-control.html', context=context)


@login_required(login_url="/login/")
def logs(request):
    context = {}
    return render(request, 'users/logs.html', context=context)


@login_required(login_url="/login/")
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'users/profile.html', context=context)