from rest_framework import serializers
from .models import Movie, Review, ReviewComment


class ReviewCommentSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    def get_userName(self,obj):
        return obj.user.username
        
    class Meta:
        model = ReviewComment
        fields = ('id', 'userName', 'user', 'content', 'review', 'rank', 'created_at', 'updated_at',)
        read_only_fields = ('user', 'review',)


class ReviewListSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    
    def get_movie_title(self, obj):
        return obj.movie.title
        
    userName = serializers.SerializerMethodField()
    
    def get_userName(self,obj):
        return obj.user.username
        
    class Meta:
        model = Review
        fields = ('id', 'user', 'userName', 'title', 'content', 'movie', 'rank', 'created_at', 'updated_at', 'movie_title')
        read_only_fields = ('user', 'movie')


class MovieSerializer(serializers.ModelSerializer):
    review_set = ReviewListSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('like_movies', 'like_users',)


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)
