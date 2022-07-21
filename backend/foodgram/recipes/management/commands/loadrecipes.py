from django.core.management.base import BaseCommand
import psycopg2

from recipes.models import Ingredient, Recipe, Tag, RecipeIngr

class Command(BaseCommand):
    def handle(self, *args, **options):
        ing = Ingredient.objects.get(id=1)
        tag = Tag.objects.get(id=1)
        for i in range(0, 7):
            recipe = Recipe.objects.create(
                name='Блюдо',
                image='recipes/fd4209fb-3121-4264-9cb7-b82fab2a4d57.png',
                text='тестовое блюдо',
                cooking_time=15,
                author_id=1
            )
            recipe.tags.add(tag)
            RecipeIngr.objects.create(
                ingredient=ing, recipe=recipe, amount=10)
        return ('Рецепты добавлены в базу данных')