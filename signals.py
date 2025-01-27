from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Album, Artist

@receiver(post_delete, sender=Album)
def delete_artist_if_no_albums(sender, instance, **kwargs):
    artist = instance.artist
    if not artist.albums.exists():
        artist.delete()