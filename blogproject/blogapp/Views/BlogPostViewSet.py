from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


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

    @action(detail=True, methods=['post'], url_path='comment', permission_classes=[IsViewer])
    def comment(self, request, pk=None):
        try:
            blog_post = self.get_object()

            from blogapp.Serializers.BlogCommentSerializer import BlogCommentSerializer

            serializer = BlogCommentSerializer(
                data=request.data,
                context={'request': request, 'blog_post': blog_post}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "status": 0,
                "message": "Comment added",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "You have already Commented on this Blog Post",
                "errors": str(e)
            }, status=status.HTTP_200_OK)