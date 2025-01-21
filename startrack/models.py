from django.db import models 
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class Artist(models.Model):
    artistID = models.AutoField(primary_key=True)  # Primary Key
    name = models.CharField(max_length=255)  # Name of the artist
    # Albums will be linked through a ForeignKey in the Album model

class Album(models.Model):
    albumID = models.AutoField(primary_key=True)  # Primary Key
    name = models.CharField(max_length=255)  # Name of the album
    year = models.PositiveIntegerField()  # Year the album was released
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")  # FK to Artist
    featured_image = CloudinaryField('image', default='placeholder')

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