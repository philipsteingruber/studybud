# Create your views here.
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic


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


def create_room(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def delete_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete_room.html', context)
