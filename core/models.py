import uuid
from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class Company(models.Model):
    """Data source for company"""
    id = models.SlugField(primary_key=True, max_length=8)
    name = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while True:
            try:
                if not self.id:
                    self.id = slugify(str(uuid.uuid4())[:8])
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
    """ユーザー"""
    MANAGER = 'manager'
    STAFF = 'staff'
    ROLE_CHOICES = [
        (MANAGER, '管理者'),
        (STAFF, '一般'),
    ]
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_password_secret = models.CharField(max_length=100, blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Client(models.Model):
    """クライアント"""
    CORPORATE = 'corporate'
    INDIVIDUAL = 'indevidual'
    CLIENT_CHOICES = [
        (CORPORATE, '法人'),
        (INDIVIDUAL, '個人'),
    ]
    id = models.SlugField(primary_key=True, max_length=8)
    code = models.CharField(blank=True)
    type = models.CharField(max_length=20, choices=CLIENT_CHOICES, blank=False)
    business_type = models.CharField(max_length=50, blank=True)
    closing_date = models.CharField(max_length=4, blank=True)
    tax_liability = models.CharField(max_length=25, blank=True)
    small_amount_exception = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True)
    kana_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    person_in_charge = models.CharField(max_length=255, blank=True)
    representative = models.CharField(max_length=255, blank=True)
    kana_representative = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey(Company, related_name='client', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while True:
            try:
                if not self.id:
                    self.id = slugify(str(uuid.uuid4())[:8])
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                continue

class History(models.Model):
    """読み取り履歴"""
    id = models.SlugField(primary_key=True, max_length=16)
    name = models.CharField(blank=True)
    ledger_type = models.CharField(max_length=50)
    num_pages = models.IntegerField(default=1)
    user = models.ForeignKey(User, related_name='history', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='history', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='history', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        while True:
            try:
                if not self.id:
                    self.id = slugify(str(uuid.uuid4())[:16])
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                continue
    def __str__(self):
        return self.name

class Result(models.Model):
    """読み取りページデータ"""
    id = models.SlugField(primary_key=True, max_length=16)
    index = models.IntegerField(default=0)
    data = models.JSONField()
    file_name = models.CharField(max_length=255, blank=True)
    filePath = models.CharField(max_length=255, blank=True)
    history = models.ForeignKey(History, related_name='result', on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return self.id


class AccountItem(models.Model):
    """勘定科目"""
    id = models.SlugField(primary_key=True, max_length=16)
    code = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    sub_account = models.CharField(max_length=255, blank=True)
    tax_class = models.CharField(max_length=20, blank=True)
    keyword = models.CharField(max_length=20, blank=True)
    in_use = models.BooleanField(default=True)
    company = models.ForeignKey(Company, related_name='accountItem', on_delete=models.CASCADE, null=True)
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
    def __str__(self):
        return self.name

class Keyword(models.Model):
    """キーワード"""
    id = models.SlugField(primary_key=True, max_length=16)
    value = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey(Company, related_name='keyword', on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return self.name