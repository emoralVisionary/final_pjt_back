from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email')
        # 응답에서 유저의 작성 리뷰 목록, 좋아요한 영화 목록을 받을 수 있지만, 유저 등록시에는 작성할 필요가 없도록
        read_only_files = ('reviews', 'like_movies')