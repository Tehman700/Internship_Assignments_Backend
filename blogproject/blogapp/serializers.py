from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


"""
For the Register Serializer, the Password field is for the authentication and since we are using User model so we defined
this in the Meta class and other fields which are necessary for Registering,
The def create function will be only called when the data is validated and we will create a new user specially with this data

"""


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'mobile_number', 'role', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


      # Below two lines are just for checking thought maybe we can use it later
      #  validated_data['password'] = make_password(validated_data['password'])  # hash password
      #  return super().create(validated_data)




"""
For the Login Serializer, only two fields required one username and other password and we use builtin function
validate to authenticate the incoming user using authenticate() method and user is valid and is active then return
otherwise make sure to defined that its invalid

"""




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError("Invalid Credentials")




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
