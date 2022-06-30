from django.http import HttpResponse
from django.shortcuts import render

from df.DFResponse import DFResponse
from songsapi.ArtistEdge import ArtistEdge


def home(request):
    return DFResponse(message="Home12", is_successful=True)


def run(request):
    for rec_raw in ArtistEdge.objects.all():
        if rec_raw.artist1 == rec_raw.artist2:
            rec_raw.delete()
    return DFResponse(message="Home12", is_successful=True)


