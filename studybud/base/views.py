# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic, Message


def login_user(request: HttpRequest) -> HttpResponse:
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').casefold()
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

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('home')


def register_user(request: HttpRequest) -> HttpResponse:
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.casefold()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid details provided for registration.')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


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
    activity_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-updated')

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'activity_messages': activity_messages}
    return render(request, 'base/home.html', context)


def view_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def user_profile(request: HttpRequest, pk: str) -> HttpResponse:
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    activity_messages = user.message_set.all().order_by('-created')
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'activity_messages': activity_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request: HttpRequest, pk: str) -> HttpResponse:
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)
