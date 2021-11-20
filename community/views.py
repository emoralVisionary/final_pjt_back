from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework import status

from .models import Post, Comment
from .serializers import PostListSerializer, CommentSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def post_list_create(request):
	# 게시글 조회
	if request.method == 'GET':
		communities = get_list_or_404(Post)
		serializer = PostListSerializer(communities, many=True)
		return Response(serializer.data)
	# 게시글 생성
	elif request.method == 'POST':
		serializer = PostListSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def post_detail(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
	serializer = PostListSerializer(Post)
	return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def post_update_delete(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
		
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



@api_view(['GET'])
def comment_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = get_list_or_404(Comment)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def comment_delete(request, post_pk, comment_pk):
	post = get_object_or_404(Post, pk=post_pk)
	comment = post.comment_set.get(pk=comment_pk)

	if not request.user.comments.filter(pk=comment_pk).exists():
		return Response({'message': '권한이 없습니다.'})
	else:
		comment.delete()
		data = {
			'id': {comment_pk}
		}
		return Response(data, status=status.HTTP_204_NO_CONTENT)