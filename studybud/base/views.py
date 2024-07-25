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
    rooms_dict = {r['id']: r for r in rooms}
    selected_room = rooms_dict.get(int(pk))
    context = {'room': selected_room}
    return render(request, 'base/room.html', context)
