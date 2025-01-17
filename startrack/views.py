from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist, Album, Track, Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


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

@login_required
def add_album_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        year = request.POST.get('year')
        artist_id = request.POST.get('artist')
        artist = get_object_or_404(Artist, pk=artist_id)
        Album.objects.create(name=name, year=year, artist=artist)
        return redirect('artist_albums', artist_id=artist.artistID)
    return render(request, 'home.html')

def album_tracks_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    tracks = album.tracks.all()
    return render(request, 'album_tracks.html', {'album': album, 'tracks': tracks})

def artist_albums_view(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    albums = artist.albums.all()
    return render(request, 'artist_albums.html', {'artist': artist, 'albums': albums})

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

@login_required
def add_track_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        Track.objects.create(name=name, album=album)
        return redirect('album_tracks', album_id=album.albumID)
    return render(request, 'album_tracks.html', {'album': album})

@login_required
def delete_track_view(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    album_id = track.album.albumID
    track.delete()
    return redirect('album_tracks', album_id=album_id)

def review_feed_view(request):
    reviews = Review.objects.select_related('track__album__artist', 'user').order_by('-id')
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'review_feed.html', {'page_obj': page_obj})