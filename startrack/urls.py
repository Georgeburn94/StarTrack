from django.urls import path, include
from .views import home_page_view, add_artist_view, add_album_view, album_tracks_view, artist_albums_view, add_rating_view, add_track_view, delete_track_view, review_feed_view, upload_album_image_view, fetch_album_details_view, delete_album_view
from django.contrib import admin
from . import views

urlpatterns = [
    path('', home_page_view, name='home'),
    path('add-artist/', add_artist_view, name='add_artist'),
    path('add-album/', add_album_view, name='add_album'),
    path('album/<int:album_id>/tracks/', album_tracks_view, name='album_tracks'),
    path('artist/<int:artist_id>/albums/', artist_albums_view, name='artist_albums'),
    path('track/<int:track_id>/add-rating/', add_rating_view, name='add_rating'),
    path('album/<int:album_id>/add-track/', add_track_view, name='add_track'),
    path('track/<int:track_id>/delete/', delete_track_view, name='delete_track'),
    path('album/<int:album_id>/delete-album/', delete_album_view, name='delete_album'),  # New URL pattern
    path('reviews/', review_feed_view, name='review_feed'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('album/<int:album_id>/upload-image/', upload_album_image_view, name='upload_album_image'),
    path('fetch-album-details/', views.fetch_album_details_view, name='fetch_album_details'),
]