"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)

# mixin is additional things you can mix in the
# view to add in functionality
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Blog, Like, Comment
from blog import serializers


class BlogViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.BlogDetailSerializer
    # added detail the reason being beside for list we want to use this
    queryset = Blog.objects.all()
    # objects that are available to the model ;Model.objects.all(), which
    #  returns a QuerySet containing all the objects in the database
    # for a particular model.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve blogs for authenticated user."""
        queryset = self.queryset
        return queryset.order_by("-id")
        # return queryset.filter(
        #     user=self.request.user
        # ).order_by('-id')
        # we get user by request from the authentication system
        # as we know user is authenticated
        # so we can filter recipe for the user that is authenticated

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.BlogSerializer
        # return reference to a class not instance
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new blog."""
        # serializer is validated
        serializer.save(user=self.request.user)

        # the reason why we have a listview and detailview is because
        # we don't want to use unnecessary resources to show details
        # every time so we default to listview

    @action(detail=True, methods=["post"], url_path="like")
    def my_likes(self, request, pk=None):
        blog = self.get_object()
        print(f"what we get :{request.data}")
        likes = request.data.pop("likes", [])
        # data = request.data
        likes = likes[0]
        serializer = serializers.LikeSerializer(data=likes)
        # print(f"this is the data being passed to serializer :{data}")
        serializer.is_valid(raise_exception=True)
        # print(f"ths is for serializer.data{serializer.data}")
        serializer.save(blog=blog, user=request.user)
        print(f"ths is for serializer.data{serializer.data}")
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="comment")
    def my_comments(self, request, pk=None):
        blog = self.get_object()
        comments = request.data.pop("comments", [])
        # data = request.data
        comments = comments[0]
        serializer = serializers.CommentSerializer(data=comments)
        serializer.is_valid(raise_exception=True)
        serializer.save(blog=blog, user=request.user)
        return Response(serializer.data)


# @api_view(["POST"])
# def add_like_or_comment(request, blog_id):
#     try:
#         blog = Blog.objects.get(id=blog_id)
#     except Blog.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # Check if user is authenticated
#     if not request.user.is_authenticated:
#         return Response(
#             {"detail": "Authentication credentials were not provided."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )

#     # Check if request is for adding a like
#     if "like" in request.data:
#         like_data = {"user": request.user, "like": True}
#         like_serializer = LikeSerializer(data=like_data)
#         if like_serializer.is_valid():
#             like = like_serializer.save()
#             blog.likes.add(like)
#             return Response(
#                 {"detail": "Like added successfully."}, status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Check if request is for adding a comment
#     if "text" in request.data:
#         comment_data = {"user": request.user, "text": request.data["text"]}
#         comment_serializer = CommentSerializer(data=comment_data)
#         if comment_serializer.is_valid():
#             comment = comment_serializer.save()
#             blog.comments.add(comment)
#             return Response(
#                 {"detail": "Comment added successfully."},
#                 status=status.HTTP_201_CREATED,
#             )
#         else:
#             return Response(
#                 comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
#             )

#     # Return error if request is not for adding a like or comment
#     return Response(
#         {"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST
# )


# class LikeViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     """Manage tags in the database."""

#     # Put Generic in last since it can override some behaviour
#     # mixin Update provides update functionality
#     serializer_class = serializers.LikeSerializer
#     queryset = Like.objects.all()

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     """Filter queryset to authenticated user."""
#     #     return self.queryset.filter(
#     #         user=self.request.user
#     #     ).order_by('-name').distinct()


# class CommentViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     """Manage tags in the database."""

#     # Put Generic in last since it can override some behaviour
#     # mixin Update provides update functionality
#     serializer_class = serializers.CommentSerializer
#     queryset = Comment.objects.all()

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     """Filter queryset to authenticated user."""
#     #     return self.queryset.filter(
#     #         user=self.request.user
#     #     ).order_by('-name').distinct()


# def get_Likes(request):
#     Likes_state = request.data['State']
#     post_id = request.data['id']
#     # post_id = int(post_id)
#     cur_count_dict = Post.objects.filter(post_id).values('current_count')
#     cur_count = cur_count_dict['current_count']
#     cur_count = int(cur_count)
#     if Likes_state == 'False':
#         cur_count -= 1
#     elif Likes_state == 'True':
#         cur_count += 1


# #     Post.objects.filter(pk=post_id).update(active=True)
# class PostViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     serializer_class = serializers.PostSerializer
#     queryset = Post.objects.all()


# class NewLikeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
#                      mixins.ListModelMixin,
#                      viewsets.GenericViewSet):
#     queryset = Like.objects.all()

#     def get_Likes(request):
#         Likes_state = request.data['State']
#         post_id = request.data['id']
#         # post_id = int(post_id)
#         cur_count_dict = Post.objects.filter(post_id).values('current_count')
#         cur_count = cur_count_dict['current_count']
#         cur_count = int(cur_count)
#         if Likes_state == 'False':
#             cur_count -= 1
#         elif Likes_state == 'True':
#             cur_count += 1

#         Post.objects.filter(pk=post_id).update(active=True)
