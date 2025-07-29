from rest_framework import serializers
from blogapp.Models.BlogCommentReaction import BlogCommentReaction

class BlogCommentReactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = BlogCommentReaction
        fields = ['id', 'user', 'reaction_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        comment = self.context['comment']
        reaction_type = validated_data['reaction_type']

        # Check if user already reacted to this comment
        existing_reaction = BlogCommentReaction.objects.filter(
            user=user, comment=comment
        ).first()

        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Same reaction - toggle off (delete)
                existing_reaction.delete()
                self.context['toggled_off'] = True
                return existing_reaction
            else:
                # Different reaction - update
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                return existing_reaction
        else:
            # New reaction
            return BlogCommentReaction.objects.create(
                user=user,
                comment=comment,
                reaction_type=reaction_type
            )