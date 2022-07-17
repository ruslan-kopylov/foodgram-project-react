from django.db import models
from django.core.validators import validate_slug, MinValueValidator
from users.models import User


class Recipe(models.Model):
    name = models.CharField(help_text='Название', max_length=200, blank=False)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=False
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    text = models.TextField(help_text='Описание', blank=False)
    cooking_time = models.PositiveSmallIntegerField(help_text='Время приготовления (в минутах)', validators=[MinValueValidator(1)], blank=False)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe, through= 'RecipeIngr')#, related_name='ingredients')


class Tag(models.Model):
    name = models.CharField(help_text='Название', max_length=200)
    color = models.CharField(help_text='цвет в НЕХ', max_length=7)
    slug = models.CharField(
        help_text='Уникальный слаг',
        max_length=200,
        validators=[validate_slug]
    )
    recipes = models.ManyToManyField(Recipe, related_name='tags')


class RecipeIngr(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.PositiveSmallIntegerField('Количество', validators=[MinValueValidator(0)])
