from django.db import models
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        max_length=254,
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    password = models.CharField(max_length=150, blank=False, null=False, error_messages={
        'detail': 'Обязательное поле',
    })
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_subscribe'
            ),
        ]