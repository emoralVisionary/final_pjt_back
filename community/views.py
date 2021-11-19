from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import PostSerializer,CommentSerializer
from .models import Post,Comment

# Create your views here.
# post 목록 조회, 생성
@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.order_by('-pk')
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    else:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

# post 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if not request.user.post.filter(pk=post_pk).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        if not request.user.post.filter(pk=post_pk).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({ 'id': post_pk }, status=status.HTTP_204_NO_CONTENT)


# @api_view(['DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def post_update_delete(request, post_pk):
# 	post = get_object_or_404(Post, pk=post_pk)
# 	if request.method == 'DELETE':
# 		post.delete()
# 		data = {
# 			'delete': f'데이터 {post_pk}번이 삭제되었습니다.'
# 		}
# 		return Response(data, status=status.HTTP_204_NO_CONTENT)





# comment 목록 조회, 생성
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_create(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    else:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,post=post)
            return Response(serializer.data,status=status.HTTP_201_CREATED)


# comment 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request,post_pk,comment_pk):
	post = get_object_or_404(Post, pk=post_pk)
	comment = get_object_or_404(Comment, pk=comment_pk)
	if request.method == 'GET':
		serializer = CommentSerializer(comment)
		return Response(serializer.data)
	elif request.method == 'PUT':
		serializer = CommentSerializer(comment, data=request.data)
		if not request.user.comment.filter(pk=comment_pk).exists():
			return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(serializer.data)
	elif request.method == 'DELETE':
		if not request.user.comment.filter(pk=comment_pk).exists():
			return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
		comment.delete()
		data = {
            'id': comment_pk,
            'delete': f'data {comment_pk} is deleted',
        }
		return Response(data, status=status.HTTP_204_NO_CONTENT)
