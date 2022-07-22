from django.core.management.base import BaseCommand
from recipes.models import Tag, Ingredient, Recipe, RecipeIngr
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tag(name='Завтрак', color='#E26C2D', slug='breakfast').save()
        Tag(name='Обед', color='#32CD32', slug='lunch').save()
        Tag(name='Ужин', color='#0000FF', slug='dinner').save()
        print('Тэги добавлены в базу данных')
        with open('/app/ingredients.json', 'rb') as file:
            data = json.load(file)
            for item in data:
                Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                ).save()
        print('Ингредиенты добавлены в базу данных')
        #ing = Ingredient.objects.get(id=1)
        #tag = Tag.objects.get(id=1)
        #for i in range(0, 7):
        #    recipe = Recipe.objects.create(
        #        name='Блюдо',
        #        image='recipes/fd4209fb-3121-4264-9cb7-b82fab2a4d57.png',
        #        text='тестовое блюдо',
        #        cooking_time=15,
        #        author_id=1
        #    )
        #    recipe.tags.add(tag)
        #    RecipeIngr.objects.create(
        #        ingredient=ing, recipe=recipe, amount=10)
        return ('Данные добавлены в базу данных')
