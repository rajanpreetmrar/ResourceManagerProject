from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission


class CustomUserManager(BaseUserManager):
    def create_user(self, fullname, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(fullname=fullname, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(fullname, username, email, password, **extra_fields)


class UserAccounts(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=255, unique=False)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=(
        ('normal', 'Normal User'),
        ('superuser', 'Super User'),
    ), default='normal')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'email']

    def __str__(self):
        return self.username

