from django.http import HttpResponse
from django.shortcuts import render

from df.DFResponse import DFResponse
from songsapi.ArtistEdge import ArtistEdge
from songsapi.views import get_all_home_page_data


def home(request):
    return DFResponse(message="Home12", is_successful=True)


def run(request):
    get_all_home_page_data(request)
    return DFResponse(message="Home12", is_successful=True)


