# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic


def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username or password is incorrect.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {}
    return render(request, 'base/login_register.html', context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('home')


def home(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q')
    if not q:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def view_room(request: HttpRequest, pk: str) -> HttpResponse:
    context = {'room': Room.objects.get(id=pk)}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room.')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete_room.html', context)
