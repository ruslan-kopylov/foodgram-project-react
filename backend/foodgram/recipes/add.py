import sqlite3

conn = sqlite3.connect('/home/ruslan/Dev/diplom/foodgram-project-react/backend/foodgram/db.sqlite3')
c = conn.cursor()
#c.execute('''INSERT INTO recipes_tag
#             VALUES(0, 'Завтрак', '#E26C2D', 'breakfast')''')
#
#c.execute('''INSERT INTO recipes_tag
#             VALUES(1, 'Обед', '##2986CC', 'Lunch')''')
#
#c.execute('''INSERT INTO recipes_ingredient
#             VALUES(0, 'Капуста', 'кг')''')
#
#c.execute('''INSERT INTO recipes_ingredient
#             VALUES(1, 'Морковка', 'кг')''')

#c.execute('''INSERT INTO recipes_recipes
#             VALUES(
#                0, 'Салат',
#                'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
#                'Режем салат', '5', '1')''')

#c.execute('''INSERT INTO recipes_recipes_tags
#             VALUES(2, 0, 1)''')
#
#c.execute('''INSERT INTO recipes_recipes_tags
#             VALUES(3, 0, 0)''')
c.execute('''DELETE FROM recipes_recipe''')
c.execute('''DELETE FROM recipes_tag_recipes''')
c.execute('''DELETE FROM recipes_recipeingr''')
#c.execute('''DELETE FROM recipes_recipe_tags''')

conn.commit()

conn.close()