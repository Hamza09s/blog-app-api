"""
Serializers for blog APIs
"""
from rest_framework import serializers

from core.models import Blog, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "text"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        print(f"this is ::::: {validated_data}")
        comments = validated_data
        blog = validated_data.pop("blog")
        auth_user = validated_data.pop("user")
        comment_obj = Comment.objects.create(text=comments)
        blog.comments.add(comment_obj)
        print(comment_obj)
        return comment_obj


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "author", "the_like"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        print(f"this is ::::: {validated_data}")
        likes = validated_data
        blog = validated_data.pop("blog")
        auth_user = validated_data.pop("user")
        like_obj = Like.objects.create(the_like=likes)
        blog.likes.add(like_obj)
        print(like_obj)
        return like_obj


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for blogs."""

    comments = CommentSerializer(many=True, required=False)
    likes = LikeSerializer(many=True, required=False)
    like_count = serializers.SerializerMethodField("get_like_count")

    class Meta:
        model = Blog
        fields = [
            "id",
            "author",
            "title",
            "category",
            "date_created",
            "likes",
            "like_count",
            "comments",
        ]
        read_only_fields = ["id", "like_count"]

    def _get_or_create_likes(self, likes, blog):
        """Handle getting or creating likes as needed."""
        auth_user = self.context["request"].user
        for like in likes:
            like_obj, created = Like.objects.get_or_create(
                user=auth_user,
                **like,
            )
            blog.likes.add(like_obj)

    def get_like_count(self, obj):
        return obj.likes.count()

    def _get_or_create_comments(self, comments, blog):
        auth_user = self.context["request"].user
        for comment in comments:
            comment_obj, created = Comment.objects.get_or_create(
                user=auth_user,
                **comment,
            )
            blog.comments.add(comment_obj)

    def create(self, validated_data):
        """Create a blog"""
        likes = validated_data.pop("likes", [])
        comments = validated_data.pop("comments", [])
        blog = Blog.objects.create(**validated_data)
        self._get_or_create_likes(likes, blog)
        self._get_or_create_comments(comments, blog)

        return blog

    def update(self, instance, validated_data):
        """Update blog."""
        likes = validated_data.pop("likes", None)
        comments = validated_data.pop("comments", None)
        # if likes is not None:
        #     instance.likes.clear()
        #     self._get_or_create_likes(likes, instance)
        # if comments is not None:
        #     instance.comments.clear()
        #     self._get_or_create_comments(comments, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class BlogDetailSerializer(BlogSerializer):
    """Serializer for blog detail view."""

    class Meta(BlogSerializer.Meta):
        fields = BlogSerializer.Meta.fields + ["content"]


# class PostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Post
#         fields = ['id', 'current_count']
#         read_only_fields = ['id']
