from rest_framework import serializers
from blogapp.Models.BlogComment import BlogComment

class BlogCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = BlogComment
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        blog_post = self.context['blog_post']
        return BlogComment.objects.create(
            user=user,
            blog_post=blog_post,
            comment=validated_data['comment']
        )
