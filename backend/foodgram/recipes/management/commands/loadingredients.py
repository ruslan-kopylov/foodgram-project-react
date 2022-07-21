from django.core.management.base import BaseCommand
import json
from recipes.models import Ingredient

class Command(BaseCommand):
    def handle(self, *args, **options):
        #with open('/home/ruslan/Dev/diplom/foodgram-project-react/backend/foodgram/ingredients.json', 'rb') as file:
        with open('/app/ingredients.json', 'rb') as file:
            data = json.load(file)

            for item in data:
                Ingredient(
                    name = item['name'],
                    measurement_unit = item['measurement_unit']
                ).save()
        return ('Ингредиенты добавлены в базу данных')