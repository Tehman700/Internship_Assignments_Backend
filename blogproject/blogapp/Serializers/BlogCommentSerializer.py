from rest_framework import serializers

from blogapp.Serializers.BlogCommentReplySerializer import BlogCommentReplySerializer
from blogapp.Models.BlogComment import BlogComment


class BlogCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()
    replies = BlogCommentReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    parent_comment_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = BlogComment
        fields = [
            'id', 'user', 'comment', 'created_at', 'replies', 'reply_count',
            'like_count', 'dislike_count', 'user_reaction', 'parent_comment_id'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def get_reply_count(self, obj):
        return obj.replies.count()

    def get_like_count(self, obj):
        return obj.reactions.filter(reaction_type='like').count()

    def get_dislike_count(self, obj):
        return obj.reactions.filter(reaction_type='dislike').count()

    def get_user_reaction(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            reaction = obj.reactions.filter(user=request.user).first()
            return reaction.reaction_type if reaction else None
        return None

    def validate(self, data):
        user = self.context['request'].user
        blog_post = self.context['blog_post']
        parent_comment_id = data.get('parent_comment_id')

        # Rule 4: Can't comment on own blog (only applies to top-level comments)
        if not parent_comment_id and blog_post.author == user:
            raise serializers.ValidationError("You cannot comment on your own blog post.")

        # If it's a reply, validate parent comment exists and belongs to the same blog post
        if parent_comment_id:
            try:
                parent_comment = BlogComment.objects.get(
                    id=parent_comment_id,
                    blog_post=blog_post,
                    parent_comment__isnull=True  # Ensure parent is a top-level comment
                )
                data['parent_comment'] = parent_comment
            except BlogComment.DoesNotExist:
                raise serializers.ValidationError("Invalid parent comment.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        blog_post = self.context['blog_post']
        parent_comment = validated_data.pop('parent_comment', None)

        return BlogComment.objects.create(
            user=user,
            blog_post=blog_post,
            parent_comment=parent_comment,
            comment=validated_data['comment']
        )