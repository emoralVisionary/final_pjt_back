from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Movie, Genre
from .serializers import MovieListSerializer, MovieSerializer
import requests
import json


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = ArticleSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def detail(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)