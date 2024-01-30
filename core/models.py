import uuid
from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class Company(models.Model):
    """Data source for embeddings"""
    id = models.SlugField(primary_key=True, max_length=16)
    name = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        while True:
            try:
                if not self.id:
                    self.id = slugify(str(uuid.uuid4())[:16])
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                continue


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=email, name=email.split('@')[0],  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    reset_password_secret = models.CharField(max_length=100, blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'