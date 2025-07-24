from rest_framework import serializers
from blogapp.Models.BlogReaction import BlogReaction


class BlogReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogReaction
        fields = ['id', 'reaction_type']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        blog_post = self.context['blog_post']
        reaction_type = validated_data['reaction_type']

        existing_reaction = BlogReaction.objects.filter(user=user, blog_post=blog_post).first()

        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Same reaction again: cancel (delete)
                existing_reaction.delete()

                self.context['toggled_off'] = True
                return existing_reaction  # Optionally return something custom here
            else:
                # Different reaction: update
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                self.context['toggled_off'] = False
                return existing_reaction
        else:
                # Create new reaction
            reaction = BlogReaction.objects.create(user=user, blog_post=blog_post, reaction_type=reaction_type)
            self.context['toggled_off'] = False
            return reaction