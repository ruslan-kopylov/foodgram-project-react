from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)


class Subscribe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author'
    )
    subscriber = models.ForeignKey(
        CustomUser,
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
