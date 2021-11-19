from rest_framework import serializers
from .models import Post , Comment

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("getUsername")

    def getUsername(self, obj):
        return obj.user.username

    class Meta:
        model=Post
        fields = ('id','title','content','created_at','updated_at','username')



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("getUsername")

    def getUsername(self, obj):
        return obj.user.username

    class Meta:
        model=Comment
        fields = ('id','content','created_at','updated_at','user_id','username','post_id')