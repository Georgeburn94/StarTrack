from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist, Album, Track, Review
from django.contrib.auth.decorators import login_required

def home_page_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        artists = Artist.objects.filter(name__icontains=search_query)
    else:
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

def album_tracks_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    tracks = album.tracks.all()
    return render(request, 'album_tracks.html', {'album': album, 'tracks': tracks})

@login_required
def add_rating_view(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    if request.method == 'POST':
        star_rating = request.POST.get('star_rating')
        note = request.POST.get('note')
        user = request.user
        review, created = Review.objects.update_or_create(
            track=track,
            defaults={'star_rating': star_rating, 'note': note, 'user': user}
        )
        return redirect('album_tracks', album_id=track.album.albumID)
    return render(request, 'album_tracks.html')