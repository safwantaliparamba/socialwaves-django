import uuid

from django.db import models
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

from general.models import BaseModel
from general.encryptions import encrypt
from general.middlewares import RequestMiddleware
from general.functions import random_password,get_auto_id,generate_unique_id


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


class UserSession(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    ip = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True,blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    system = models.CharField(max_length=255, null=True, blank=True)
    system_meta_data = models.TextField(null=True, blank=True)
    date_signed_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'accounts_user_session'
        verbose_name = 'user_session'
        verbose_name_plural = 'user_sessions'
        ordering = ('-date_added',)

    def __str__(self):
        return self.ip
    


CHIEF_PRFILE_TYPES = [
    ("chief","Chief")
]
    

class ChiefProfile(BaseModel):
    user = models.OneToOneField(User,related_name="chief",on_delete=models.CASCADE,null=True,blank=True)

    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    profile_type = models.CharField(choices=CHIEF_PRFILE_TYPES,default='chief',max_length=128)
    name = models.CharField(max_length=128,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=30,null=True, blank=True)

    class Meta:
        db_table = "users_chief_profile"
        verbose_name = "Chief Profile"
        verbose_name_plural = "Chief Profiles"
        ordering = ('auto_id',)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):

        if self._state.adding:
            request = RequestMiddleware(get_response=None)
            request:HttpRequest = request.thread_local.current_request

            chief_password = self.password
            chief_username = self.username
            
            if not chief_password:
                chief_password = random_password(12)

            if not chief_username:
                chief_username = generate_unique_id(12)

            user = self.user

            if not user:
                user = User.objects.create_user(
                    email=self.email,
                    password=chief_password,
                    name=self.name,
                    encrypted_password=encrypt(chief_password),
                )
                self.user = user

            elif self.user:
                self.user.set_password(chief_password)
                self.user.save()

            if self.profile_type == 'chief':
                usergroup, created = Group.objects.get_or_create(name="chief")
                usergroup.user_set.add(user)

            self.auto_id = get_auto_id(ChiefProfile)
            self.password = encrypt(chief_password)
            self.creator = request.user
            self.updater = request.user 


        super(ChiefProfile,self).save(*args, **kwargs)