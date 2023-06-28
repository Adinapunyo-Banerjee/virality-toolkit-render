from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('isPremium', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff true'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14, null=True, blank=True)
    isPremium = models.BooleanField(default=False)
    isPromotable = models.BooleanField(default=True)
    PremiumBuyDate = models.DateTimeField(null=True, blank=True)
    PremiumExpiryDate = models.DateTimeField(null=True, blank=True)
    totalPredictions = models.IntegerField(default=0)
    tokenBalance = models.IntegerField(default=100)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
