from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Movie, Review, ReviewComment, Genre
from .serializers import MovieSerializer, MovieListSerializer, ReviewListSerializer, ReviewCommentSerializer
import requests
import json


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def list(request):
    if request.method == 'GET':
        # 전체 영화 리스트 가져오기
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = ArticleSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', ])
# @permission_classes([AllowAny])
def detail(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
# 리뷰 조회/작성
def review_list_create(request, movie_pk):
    if request.method == 'GET':
        reviews = get_list_or_404(Review, movie_id=movie_pk)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid():
        # if serializer.is_valid(raise_exception=True):
            movie = get_object_or_404(Movie, pk=movie_pk)
            # movie.save()        
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)


@api_view(['PUT', 'DELETE'])
# 리뷰 수정/삭제
def review_update_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'PUT':
        serializer = ReviewListSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            movie = get_object_or_404(Movie, pk=movie_pk)
            # movie.save()
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
        return Response({ 'id': review_pk })


@api_view(['GET', 'POST'])
# 리뷰에 대한 댓글 조회/작성
def review_comment_list_create(request, review_pk):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk=review_pk)
        comments = review.reviewcomment_set.all()
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
# 리뷰 댓글 삭제
def review_comment_delete(request, review_pk, review_comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = review.reviewcomment_set.get(pk=review_comment_pk)
    comment.delete()    
    return Response({ 'id': review_comment_pk })