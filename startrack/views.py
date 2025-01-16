from django.shortcuts import render, redirect
from .models import Artist, Album

# Create your views here.
def home_page_view(request):
    artists = Artist.objects.all()
    return render(request, 'home.html', {'artists': artists})

def add_artist_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        Artist.objects.create(name=name, bio=bio)
        return redirect('home')
    return render(request, 'home.html')

def add_album_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        year = request.POST.get('year')
        artist_id = request.POST.get('artist')
        artist = Artist.objects.get(artistID=artist_id)
        Album.objects.create(name=name, year=year, artist=artist)
        return redirect('home')
    return render(request, 'home.html')