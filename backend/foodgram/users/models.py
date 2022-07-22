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
    favorites = models.ManyToManyField(
        'recipes.Recipe', through='recipes.Favorite',
        related_name='favorites', blank=True)
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe', through='recipes.ShoppingCart',
        related_name='shopping_cart', blank=True)


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
