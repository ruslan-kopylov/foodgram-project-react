from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        method='ingredient'
    )

    def ingredient(self, queryset, name, value):
        result_1 = Ingredient.objects.filter(name__iregex=fr'^{value}')
        result_2 = Ingredient.objects.filter(name__iregex=fr'\s{value}')
        result = result_1 | result_2
        return result


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        label='tags',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_shopping_cart'
    )

    def filter_favorited(self, queryset, name, value):
        return self.request.user.favorites.all().filter(pk__in=queryset)

    def filter_shopping_cart(self, queryset, name, value):
        return self.request.user.shopping_cart.all()

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')
