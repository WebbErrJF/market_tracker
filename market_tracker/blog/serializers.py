from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    author_id = serializers.IntegerField(source='author.id')

    class Meta:
        model = Comment
        fields = '__all__'


class SaveCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
