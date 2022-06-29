from django.http import HttpResponse
from django.shortcuts import render

from df.DFResponse import DFResponse
from df.forms import AudioForm
from songsapi.ArtistEdge import ArtistEdge


def home(request):
    return DFResponse(message="Home12", is_successful=True)


def run(request):
    for rec_raw in ArtistEdge.objects.all():
        if rec_raw.artist1 == rec_raw.artist2:
            rec_raw.delete()
    return DFResponse(message="Home12", is_successful=True)


def audio_store(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
    else:
        form = AudioForm()
    return render(request, 'aud.htm', {'form': form})
