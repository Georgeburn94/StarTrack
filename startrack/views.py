from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist, Album, Track, Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .spotify_utility import get_token, search_for_album, get_album_tracks_with_details
@csrf_exempt
def import_album(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = parse_spotify_data_to_models(data)
            return JsonResponse({'success': True, 'message': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def fetch_album_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            album_query = data.get('album_query')
            if not album_query:
                return JsonResponse({'error': 'No search query provided'})
            
            token = get_token()
            album_result = search_for_album(token, album_query)
            
            if album_result:
                album_id = album_result['id']
                album_details = get_album_tracks_with_details(token, album_id)
                return JsonResponse({
                    'name': album_details['album_name'],
                    'artist': album_details['album_artist'],
                    'year': album_details['release_year'],
                    'cover_image': album_details['cover_image'],
                    'tracks': album_details['tracks']
                })
            return JsonResponse({'error': 'Album not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})


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
        try:
            data = json.loads(request.body)
            # Create or get artist
            artist, created = Artist.objects.get_or_create(
                name=data.get('artist')
            )
            # Create album
            album = Album.objects.create(
                name=data.get('name'),
                year=data.get('year'),
                artist=artist,
                featured_image=data.get('cover_image')
            )
            # Create tracks if they exist
            if 'tracks' in data:
                for track in data['tracks']:
                    Track.objects.create(
                        name=track['track_name'],
                        album=album
                    )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


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

@login_required
def delete_album_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    # Store artist reference before deletion
    artist = album.artist
    album.delete()
    # Redirect to artist's album list if artist still exists, otherwise home
    if Artist.objects.filter(pk=artist.artistID).exists():
        return redirect('artist_albums', artist_id=artist.artistID)
    return redirect('home')