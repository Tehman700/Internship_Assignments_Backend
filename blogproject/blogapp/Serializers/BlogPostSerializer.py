from rest_framework import serializers
from blogapp.Models import BlogPost, BlogReaction,BlogComment
import BlogCommentSerializer

"""
For the BlogPost Serializer, the author field was to be fetched from source and others are just normally same as we
import from Meta class the Model name is BlogPost in the model.py file and the other required fields

"""
class BlogPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'content', 'publication_date', 'author',
            'likes_count', 'dislikes_count', 'comments'
        ]

    def get_likes_count(self, obj):
        return BlogReaction.objects.filter(blog_post=obj, reaction_type='like').count()

    def get_dislikes_count(self, obj):
        return BlogReaction.objects.filter(blog_post=obj, reaction_type='dislike').count()

    def get_comments(self, obj):
        comments = BlogComment.objects.filter(blog_post=obj)
        return BlogCommentSerializer(comments, many=True).data