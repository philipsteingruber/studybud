# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import RoomForm
from .models import Room


def home(request: HttpRequest) -> HttpResponse:
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str) -> HttpResponse:
    context = {'room': Room.objects.get(id=pk)}
    return render(request, 'base/room.html', context)


def create_room(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
