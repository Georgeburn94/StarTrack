from django.urls import path, include
from .views import home_page_view, add_artist_view, add_album_view
from django.contrib import admin

urlpatterns = [
    path('', home_page_view, name='home'),
    path('add-artist/', add_artist_view, name='add_artist'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('add-album/', add_album_view, name='add_album'),
]