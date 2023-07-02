from django.db import models

# Create your models here.

from datetime import datetime

CATEGORY_CHOICES = [
    (1 , 'Film and Animation'),
    (2 , 'Autos and Vehicles'),
    (10 , 'Music'),
    (15 , 'Pets and Animals'),
    (17 , 'Sports'),
    (18 , 'Short Movies'),
    (19 , 'Travel and Events'),
    (20 , 'Gaming'),
    (21 , 'Video Blogging'),
    (22 , 'People and Blogs'),
    (23 , 'Comedy'),
    (24 , 'Entertainment'),
    (25 , 'News and Politics'),
    (26 , 'Howto and Style'),
    (27 , 'Education'),
    (28 , 'Science and Technology'),
    (29 , 'Nonprofits and Activism'),
    (30 , 'Movies'),
    (31 , 'Anime/Animation'),
    (32 , 'Action/Adventure'),
    (33 , 'Classics'),
    (34 , 'Comedy'),
    (35 , 'Documentary'),
    (36 , 'Drama'),
    (37 , 'Family'),
    (38 , 'Foreign'),
    (39 , 'Horror'),
    (40 , 'Sci-Fi/Fantasy'),
    (41 , 'Thriller'),
    (42 , 'Shorts'),
    (43 , 'Shows'),
    (44 , 'Trailer')
]

from django.conf import settings

class reviewModel(models.Model):
    title = models.CharField(max_length=50)
    email = models.EmailField()
    review = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title}  =>  {self.review}"


class predictionModel1(models.Model):
    thumb = models.ImageField(upload_to='prediction_model1')
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    subscribers = models.IntegerField(default=0)
    channel_pub_time = models.DateTimeField(default=datetime.now, blank=True)       # Passing reference to the function!
    video_pub_time = models.DateTimeField(default=datetime.now, blank=True)
    videos = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)