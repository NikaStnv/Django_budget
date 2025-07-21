from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser should be superuser status')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser should be superuser status')
        return self.create_user(email, password, **extra_fields)

    def active_user(self):
        return self.filter(is_active=True)



class AppUsers(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    phone = models.CharField('phone namber', max_length=10, unique=True, blank=True)
    date_of_birth = models.DateField('date of birth', null=True, blank=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=50, blank=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    date_joined = models.DateField('joining date', auto_now_add=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()




# Create your models here.
