"""
Database models.
"""
# import uuid
# import os

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        # spelling is important otherwise django cli won't pick it
        # check these lines when issue with django admin login
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Blog(models.Model):
    """Blog object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    likes = models.ManyToManyField(
        "Like",
        related_name="likes",
        default=None,
    )
    comments = models.ManyToManyField("Comment")

    @property
    def author(self):
        return self.user.name

    def __str__(self):
        return self.title


class Like(models.Model):
    """For liking a blog."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None, null=True)
    the_like = models.CharField(max_length=255, default=None, null=True)

    @property
    def author(self):
        return self.user.name

    def __str__(self):
        return f"liked"


class Comment(models.Model):
    """For commenting on a blog."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True
    )
    text = models.TextField(blank=True)

    @property
    def author(self):
        return self.user.name

    def __str__(self):
        return f"commented"


# class Post(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE, default=None, null=True
#     )
#     current_count = models.PositiveIntegerField(default=0)
