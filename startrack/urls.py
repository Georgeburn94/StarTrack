from django.urls import path, include
from .views import home_page_view, add_artist_view, add_album_view, album_tracks_view, add_rating_view
from django.contrib import admin

urlpatterns = [
    path('', home_page_view, name='home'),
    path('add-artist/', add_artist_view, name='add_artist'),
    path('add-album/', add_album_view, name='add_album'),
    path('album/<int:album_id>/tracks/', album_tracks_view, name='album_tracks'),
    path('track/<int:track_id>/add-rating/', add_rating_view, name='add_rating'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]