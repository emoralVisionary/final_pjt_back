from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework import status

from .models import Post, Comment
from .serializers import PostListSerializer, CommentSerializer

# Create your views here.
@api_view(['GET', 'POST'])
# 게시글 목록 조회는 누구나 가능
@permission_classes([AllowAny])
def post_list(request):
	# 게시글 목록 조회
	if request.method == 'GET':
		communities = get_list_or_404(Post)
		serializer = PostListSerializer(communities, many=True)
		return Response(serializer.data)


@api_view(['POST'])
# 로그인 한 사람만 게시글 작성 가능
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_create(request):
    # 게시글 생성
    if request.method == 'POST':
        serializer = PostListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# 로그인 한 사람만 게시글 내용 조회 가능
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
	serializer = PostListSerializer(post)
	return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_update_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 글 작성자만 게시글 수정/삭제 가능
    if not request.user.posts.filter(pk=post_pk).exists():
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = PostListSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        data = {
            'id': {post_pk}
		}
        return Response(data, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_create(request, post_pk):
    # 게시글에 대한 댓글 목록
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        # comments = get_list_or_404(post)
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    # 게시글에 대한 댓글 생성
    elif request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, post_pk, comment_pk):
	post = get_object_or_404(Post, pk=post_pk)
	comment = post.comment_set.get(pk=comment_pk)
    # 댓글 작성자만 삭제 가능하도록
	if not request.user.comment_set.filter(pk=comment_pk).exists():
		return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
	else:
		comment.delete()
		data = {
			'id': {comment_pk}
		}
		return Response(data, status=status.HTTP_204_NO_CONTENT)