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

from core.models import (
    Blog,
)
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
        return queryset.filter(
            user=self.request.user
        ).order_by('-id')
        # we get user by request from the authentication system
        # as we know user is authenticated
        # so we can filter recipe for the user that is authenticated

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
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
