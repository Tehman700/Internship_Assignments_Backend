from rest_framework import serializers
from blogapp.Models.BlogComment import BlogComment

class BlogCommentReplySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        fields = ['id', 'user', 'comment', 'created_at', 'like_count', 'dislike_count', 'user_reaction']
        read_only_fields = ['id', 'user', 'created_at']


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