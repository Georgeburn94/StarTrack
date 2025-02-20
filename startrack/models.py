from django.db import models 
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Artist(models.Model):
    artistID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def delete_if_no_albums(self):
        # Get fresh count from database
        if not Album.objects.filter(artist=self).exists():
            self.delete()
            
    def __str__(self):
        return self.name

class Album(models.Model):
    albumID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE,
        related_name="albums"
    )
    featured_image = models.URLField(max_length=200, blank=True, null=True)

    def delete(self, *args, **kwargs):
        artist = self.artist
        super().delete(*args, **kwargs)
        # Get fresh instance of artist to check albums
        if not Album.objects.filter(artist=artist).exists():
            artist.delete()

    def __str__(self):
        return self.name


class Track(models.Model):
    trackID = models.AutoField(primary_key=True)  # Primary Key
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="tracks")  # FK to Album
    name = models.CharField(max_length=255)  # Name of the track

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")  # FK to User
    track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name="review")  # One-to-One relationship with Track
    star_rating = models.PositiveSmallIntegerField()  # Star Rating (e.g., 1-5)
    note = models.TextField(blank=True, null=True)  # Optional note

    def __str__(self):
        return f"{self.track.name} - {self.star_rating} stars"