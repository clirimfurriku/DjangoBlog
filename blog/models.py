from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, user_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        elif not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_type=user_type or 'r',  # By default make the user reader
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_type, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            user_type=user_type or 'a',  # By default make the superuser author
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    # Basic User fields (https://docs.djangoproject.com/en/3.1/topics/auth/customizing/)
    email = models.EmailField(
        verbose_name='email address',
        max_length=120,
        unique=True,
    )
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type']

    # There will be three types of users:
    # 1 - Moderator (Can publish articles, edit, comment)
    # 2 - Authors (Can publish articles, comment)
    # 3 - Reader (Can comment on articles)
    USER_CHOICES = (
        ('m', 'Moderator'),
        ('a', 'Author'),
        ('r', 'Reader')
    )
    user_type = models.CharField(
        max_length=1,
        choices=USER_CHOICES,
        null=True,
        blank=True
    )
    bio = models.CharField(max_length=2048, null=True, blank=True)
    # Social profiles
    twitter = models.CharField(max_length=128, null=True, blank=True)
    instagram = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)  # profile pic

    def __str__(self):
        return f'{self.username or "Unknown"}'

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.TextField(max_length=1024)
    content = models.TextField()  # TODO: Check if html i supported
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    thumbnail_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.title} {self.updated_date}'


class UserComment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} {self.comment_date}'
