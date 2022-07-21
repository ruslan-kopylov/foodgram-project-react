from core.models import CreatedModel
from django.core.validators import MinValueValidator, validate_slug
from django.db import models
from users.models import CustomUser


class Recipe(CreatedModel):
    name = models.CharField(help_text='Название', max_length=200, blank=False)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=False
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes')
    text = models.TextField(help_text='Описание', blank=False)
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
        blank=False
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe, through='RecipeIngr')


class Tag(models.Model):
    name = models.CharField(help_text='Название', max_length=200)
    color = models.CharField(help_text='цвет в НЕХ', max_length=7)
    slug = models.SlugField(
        help_text='Уникальный слаг',
        max_length=200,
        validators=[validate_slug]
    )
    recipes = models.ManyToManyField(Recipe, related_name='tags')


class RecipeIngr(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[MinValueValidator(0)])


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
