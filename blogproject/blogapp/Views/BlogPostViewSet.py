from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from blogapp.Models.BlogComment import BlogComment


class BlogPostViewSet(viewsets.ModelViewSet):
    from blogapp.Serializers.BlogPostSerializer import BlogPostSerializer

    serializer_class = BlogPostSerializer
    permission_classes = []



# Normally we use builtin queryset for fetching all the users, but we have some restrictions so created separate function
    def get_queryset(self):
        user = self.request.user                                # the particular user
        from blogapp.Models.BlogPost import BlogPost
        if user.is_authenticated:                               # if is validated and authenticated, it covers all JWT
            if user.role == 'writer':                           # if writer
                return BlogPost.objects.filter(author=user)     # filter out the object of that user as author = user
            return BlogPost.objects.all()                       # viewer sees all
        return BlogPost.objects.none()                          # return empty if nothing

# The above function just gets the raw queryset to view it we use below function

    def list(self, request):  # Called when GET /api/blogs/
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)  # Converts to list of dictionaries
            return Response({

                # Message
                "status": 0,
                "message": "Blog posts fetched successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error in fetching posts",
                "errors": str(e)
            }, status=200)
# debug for printing states, yotube

# Retrieve function is called when we want to get specific id or blogpost with id
    def retrieve(self, request, *args, **kwargs):  # GET /api/blogs/<id>/
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": 0,
                "message": "Post retrieved successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error retrieving blog post",
                "errors": str(e)
            }, status=200)





    def create(self, request, *args, **kwargs):
        # Check custom permission manually to control the response
        from blogapp.Views.IsWriterOrReadOnly import IsWriterOrReadOnly

        permission = IsWriterOrReadOnly()
        if not permission.has_permission(request, self):
            return Response({
                "status": 1,
                "message": "You are not allowed, you are a viewer"
            }, status=status.HTTP_200_OK)

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)

            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response({
                    "status": 0,
                    "message": "Blog post created",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "status": 1,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error during creation",
                "errors": str(e)
            }, status=status.HTTP_200_OK)




    def update(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            instance = self.get_object()
            if instance.author != request.user:
                return Response({
                    "status": 1,
                    "message": "You are not allowed to update this post"
                }, status=200)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 0,
                    "message": "Blog post updated",
                    "data": serializer.data
                }, status=200)
            return Response({
                "status": 1,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error during update",
                "errors": str(e)
            }, status=200)




    def destroy(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            instance = self.get_object()
            if instance.author != request.user:
                return Response({
                    "status": 1,
                    "message": "You are not allowed to delete this post"
                }, status=200)

            # If correct user
            instance.delete()
            return Response({
                "status": 0,
                "message": "Blog post deleted"
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error deleting blog post",
                "errors": str(e)
            }, status=200)
    from blogapp.Utils.permissions import IsViewer
    from rest_framework.decorators import action

    @action(detail=True, methods=['post'], url_path='like', permission_classes=[IsViewer])
    def like(self, request, pk=None):
        try:
            blog_post = self.get_object()
            from blogapp.Serializers.BlogReactionSerializer import BlogReactionSerializer

            serializer = BlogReactionSerializer(
                data={'reaction_type': 'like'},
                context={'request': request, 'blog_post': blog_post}
            )
            serializer.is_valid(raise_exception=True)
            reaction = serializer.save()
            toggled_off = serializer.context.get('toggled_off', False)

            return Response({
                "status": 0,
                "message": "Like removed" if toggled_off else "Liked successfully",
                "data": BlogReactionSerializer(reaction).data if not toggled_off else {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error while liking the post",
                "errors": str(e)
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='dislike', permission_classes=[IsViewer])
    def dislike(self, request, pk=None):
        try:
            blog_post = self.get_object()
            from blogapp.Serializers.BlogReactionSerializer import BlogReactionSerializer

            serializer = BlogReactionSerializer(
                data={'reaction_type': 'dislike'},
                context={'request': request, 'blog_post': blog_post}
            )
            serializer.is_valid(raise_exception=True)
            reaction = serializer.save()
            toggled_off = serializer.context.get('toggled_off', False)

            return Response({
                "status": 0,
                "message": "Dislike removed" if toggled_off else "Disliked successfully",
                "data": BlogReactionSerializer(reaction).data if not toggled_off else {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error while disliking the post",
                "errors": str(e)
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='comment')
    def comment(self, request, pk=None):
        """Add a comment or reply to a blog post"""
        try:
            blog_post = self.get_object()
            from blogapp.Serializers.BlogCommentSerializer import BlogCommentSerializer

            serializer = BlogCommentSerializer(
                data=request.data,
                context={'request': request, 'blog_post': blog_post}
            )
            serializer.is_valid(raise_exception=True)
            comment = serializer.save()

            return Response({
                "status": 0,
                "message": "Reply added" if comment.parent_comment else "Comment added",
                "data": BlogCommentSerializer(comment, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": -1,
                "message": str(e),
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        """Get all comments for a blog post"""
        try:
            blog_post = self.get_object()
            # Only get top-level comments (replies are included via serializer)
            comments = BlogComment.objects.filter(
                blog_post=blog_post,
                parent_comment__isnull=True
            ).order_by('-created_at')

            from blogapp.Serializers.BlogCommentSerializer import BlogCommentSerializer
            serializer = BlogCommentSerializer(
                comments,
                many=True,
                context={'request': request}
            )

            return Response({
                "status": 0,
                "message": "Comments retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error retrieving comments",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='comments/(?P<comment_id>[^/.]+)/like')
    def like_comment(self, request, pk=None, comment_id=None):
        """Like a comment"""
        try:
            comment = get_object_or_404(BlogComment, id=comment_id)
            from blogapp.Serializers.BlogCommentSerializer import BlogCommentReactionSerializer

            serializer = BlogCommentReactionSerializer(
                data={'reaction_type': 'like'},
                context={'request': request, 'comment': comment}
            )
            serializer.is_valid(raise_exception=True)
            reaction = serializer.save()
            toggled_off = serializer.context.get('toggled_off', False)

            return Response({
                "status": 0,
                "message": "Like removed from comment" if toggled_off else "Comment liked successfully",
                "data": BlogCommentReactionSerializer(reaction,
                                                      context={'request': request}).data if not toggled_off else {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error while liking the comment",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='comments/(?P<comment_id>[^/.]+)/dislike')
    def dislike_comment(self, request, pk=None, comment_id=None):
        """Dislike a comment"""
        try:
            comment = get_object_or_404(BlogComment, id=comment_id)
            from blogapp.Serializers.BlogCommentSerializer import BlogCommentReactionSerializer

            serializer = BlogCommentReactionSerializer(
                data={'reaction_type': 'dislike'},
                context={'request': request, 'comment': comment}
            )
            serializer.is_valid(raise_exception=True)
            reaction = serializer.save()
            toggled_off = serializer.context.get('toggled_off', False)

            return Response({
                "status": 0,
                "message": "Dislike removed from comment" if toggled_off else "Comment disliked successfully",
                "data": BlogCommentReactionSerializer(reaction,
                                                      context={'request': request}).data if not toggled_off else {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error while disliking the comment",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)