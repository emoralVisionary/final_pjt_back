from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.serializers import Serializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Movie, Review, ReviewComment, Genre
from .serializers import MovieSerializer, MovieListSerializer, ReviewListSerializer, ReviewCommentSerializer
import requests
import json
from django.db.models import Q
from datetime import date

from django.core.paginator import Paginator


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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


# 검색
@api_view(['POST'])
def search(request):
    keyword = request.data.get('keyword')
    movies = Movie.objects.filter(Q(title__icontains=keyword)|Q(original_title__icontains=keyword))
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


        


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_list_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 리뷰 조회/작성
    if request.method == 'GET':
        reviews = get_list_or_404(Review, movie_id=movie_pk)
        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page_num')
        reviews = paginator.get_page(page_number)
        serializer = ReviewListSerializer(reviews, many=True)
        data = serializer.data
        data.append({'possible_page': paginator.num_pages})
        return Response(data)
    elif request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        # if serializer.is_valid():
        if serializer.is_valid(raise_exception=True):
            # movie = get_object_or_404(Movie, pk=movie_pk)
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
    review = get_object_or_404(Review, pk=review_pk)
    # 리뷰에 대한 댓글 조회/작성
    if request.method == 'GET':
        comments = review.reviewcomment_set.all()
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend(request):
    # 최신 영화 추천
    newest_movies = Movie.objects.all().order_by('-release_date')[:10]
    new_serializer = MovieSerializer(newest_movies, many=True)

    # 평점 순 추천
    rated_movies = Movie.objects.all().order_by('-vote_average')[:10]
    rate_serializer = MovieSerializer(rated_movies, many=True)

    # 날씨 기준 영화 추천(장르)
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params ={
        'serviceKey' : 'KcYFmGjup0o8A5fEKjpIh3+kNtnQRnb/o8ZYCeRKYhU7+PyoTGb2PnKbdwsZ9Vb8Zm4B3QpHs2WkkcznXf67yw==',
        'pageNo' : '1',
        'numOfRows' : '12', 
        'dataType' : 'JSON', 
        'base_date' : str(date.today()).replace('-',''), 
        'base_time' : '0500', 
        'nx' : '61', 
        'ny' : '127' 
    }

    response = requests.get(url, params=params)
    content = response.content.decode("utf-8").replace("'", '"')
    # 날씨 상태 나타내는 숫자 추출 (1: 맑음, 2: 구름 조금, 3: 구름 많음, 4: 흐림)
    jsondata = json.loads(content)['response']['body']['items']['item'][5]['fcstValue']

    if jsondata == '1':
        data = {
            'Msg': '맑음',
            'genre': 80
        }
    elif jsondata == '2':
        data = {
            'Msg': '구름 조금',
            'genre': 53
        }
    elif jsondata == '3':
        data = {
            'Msg': '구름 많음',
            'genre': 27
        }
    elif jsondata == '4':
        data = {
            'Msg': '흐림',
            'genre': 10749
        }
    else:
        data = {
            'Msg': 'error'
        }
    print(data['genre'])
    
    # now_genre = Genre.objects.get(pk=data['genre'])
    now_genre = Genre.objects.get(pk="28")
    print(now_genre)
    # 해당 장르 영화 중에서 평점 높은 영화 10개 => movies
    movies = now_genre.movie_set.order_by('-vote_average')[:10]
    print(movies)
    serializer = MovieSerializer(movies, many=True)

    return Response([new_serializer.data, rate_serializer.data, serializer.data])