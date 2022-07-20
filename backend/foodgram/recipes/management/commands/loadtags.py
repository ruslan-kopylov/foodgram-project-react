from django.core.management.base import BaseCommand
import psycopg2

class Command(BaseCommand):
    def handle(self, *args, **options):
        connection = psycopg2.connect(
            user='postgres', password='postgres',
            host='db', port='5432', database='postgres'
        )
        cursor = connection.cursor()
        cursor.execute('''insert into recipes_tag (name, color, slug) values ('Завтрак', '#E26C2D', 'breakfast')''')
        cursor.execute('''insert into recipes_tag (name, color, slug) values ('Обед', '#32CD32', 'lunch')''')
        cursor.execute('''insert into recipes_tag (name, color, slug) values ('Ужин', '#0000FF', 'dinner')''')
        connection.commit()        
        return ('Тэги добавлены в базу данных')
