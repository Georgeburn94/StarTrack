from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist, Album, Track, Review
from .spotify_utility import get_token, search_for_album, get_album_tracks_with_details, parse_spotify_data_to_models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
def fetch_album_details_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        album_id = data.get('album_id')
        if album_id:
            token = get_token()
            result = search_for_album(token, album_id)
            if result:
                album_id = result["id"]
                album_details = get_album_tracks_with_details(token, album_id)
                return JsonResponse(album_details)
            else:
                return JsonResponse({'error': 'Album not found'}, status=404)
        else:
            return JsonResponse({'error': 'No album ID provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
        data = json.loads(request.body)
        name = data.get('name')
        artist_name = data.get('artist')
        year = data.get('year')
        cover_image = data.get('cover_image')

        artist, created = Artist.objects.get_or_create(name=artist_name)
        Album.objects.create(name=name, year=year, artist=artist, featured_image=cover_image)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

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

@csrf_exempt
@login_required
def upload_album_image_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        image_url = data.get('imageUrl')
        if image_url:
            album.featured_image = image_url
            album.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'No image URL provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})