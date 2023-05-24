import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager 

from general.encryptions import encrypt
from general.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError(_('The Email field must be set.'))
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=128,null=True, blank=True,unique=True)
    name = models.CharField(max_length=128,null=True,blank=True)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_TFA_activated = models.BooleanField(default=False) # two factor authentication
    image = models.ImageField(upload_to="accounts/profile/", null=True, blank=True)
    encrypted_password = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email
    


class ProfileActivity(BaseModel):
    visitor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='activity')
    profile = models.ForeignKey(User, on_delete=models.CASCADE,related_name='profile_activity')

    class Meta:
        db_table = 'accounts_profile_activity'
        verbose_name = 'profile_activity'
        verbose_name_plural = 'profile_activities'
        ordering = ('-date_added',)

    def __str__(self):
        return self.visitor.email
