# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

rooms = [
    {'id': 1, 'name': "Let's learn Python!"},
    {'id': 2, 'name': "Let's learn C!"},
    {'id': 3, 'name': "Let's learn Java!"},
]


def home(request: HttpRequest) -> HttpResponse:
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request: HttpRequest, pk: str) -> HttpResponse:
    room = None
    for possible_room in rooms:
        if possible_room['id'] == int(pk):
            room = possible_room
            break
    context = {'room': room}
    return render(request, 'base/room.html', context)
