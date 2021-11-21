from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Movie, Review, ReviewComment, Genre
from .serializers import MovieSerializer, MovieListSerializer, ReviewListSerializer, ReviewCommentSerializer
import requests
import json


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def index(request):
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_list_create(request, movie_pk):
    # 리뷰 조회/작성
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_update_delete(request, movie_pk, review_pk):
    # 리뷰 수정/삭제
    review = get_object_or_404(Review, pk=review_pk)

    if not request.user.reviews.filter(pk=review_pk).exists():
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

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
        data = { 
            'id': {review_pk} 
            }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_comment_list_create(request, review_pk):
    # 리뷰에 대한 댓글 조회/작성
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

    if not request.user.review_comments.filter(pk=review_comment_pk).exists():
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()    
    data = { 
            'id': {review_comment_pk} 
            }
    return Response(data, status=status.HTTP_204_NO_CONTENT)