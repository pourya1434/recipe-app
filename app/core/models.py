from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create, Save and Return a new user"""
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # too long
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
