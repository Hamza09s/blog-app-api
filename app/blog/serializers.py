"""
Serializers for blog APIs
"""
from rest_framework import serializers

from core.models import (
    Blog,
)


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for blogs."""

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'category', 'date_created']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a blog"""
        blog = Blog.objects.create(**validated_data)
        return blog


class BlogDetailSerializer(BlogSerializer):
    """Serializer for blog detail view."""

    class Meta(BlogSerializer.Meta):
        fields = BlogSerializer.Meta.fields + ['content']
