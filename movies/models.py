from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    # user:Movie = M:N
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    # Genre:Movie = M:N
    genre_ids = models.ManyToManyField(Genre)

    poster_path = models.CharField(max_length=200, blank=True, null=True)
    adult = models.BooleanField()
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    original_title = models.CharField(max_length=100)
    original_language = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    popularity = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)


class Review(models.Model):
	# user:review = 1:N
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
	# movie:review = 1:N
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

	title = models.CharField(max_length=100)
	content = models.TextField()
	rank = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class ReviewComment(models.Model):
	# user:reviewComment = 1:N
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_comments")
	# review:reviewComment = 1:N
	review = models.ForeignKey(Review, on_delete=models.CASCADE)

	content = models.TextField()
	rank = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)