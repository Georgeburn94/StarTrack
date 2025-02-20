from django.contrib import admin
from .models import Artist, Album, Track, Review


class AlbumAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        # Get all affected artists before deletion
        artists = set(queryset.values_list('artist_id', flat=True))
        # Delete the albums
        queryset.delete()
        # Check each artist and delete if no albums remain
        for artist_id in artists:
            try:
                artist = Artist.objects.get(pk=artist_id)
                if not artist.albums.exists():
                    artist.delete()
            except Artist.DoesNotExist:
                pass


# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Review)