import csv

from django.http import HttpResponse
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Subscribe

from .filters import RecipeFilter, IngredientFilter
from .mixins import CreateDestroyModelMixin
from .paginations import RecipePagination
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          IngrRecipeSerializerGet, RecipeSerializerGet,
                          RecipeSerializerPost, ShoppingCartSerializer,
                          SubscribeSerializer, SubscriptionsSerializer,
                          TagSerializer)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter



class RecipesViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializerGet
        if self.request.method in ('POST', 'PATCH'):
            return RecipeSerializerPost


class SubscribesListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(author__subscriber=self.request.user)


class SubscribesView(CreateDestroyModelMixin):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        author = CustomUser.objects.get(id=self.kwargs['id'])
        serializer.save(author=author, subscriber=self.request.user)

    def get_object(self):
        if self.request.method == 'POST':
            return CustomUser.objects.get(id=self.kwargs['id'])
        if self.request.method == 'DELETE':
            return Subscribe.objects.get(author_id=self.kwargs['id'])


class FavoriteView(CreateDestroyModelMixin):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorites

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        if self.request.method == 'DELETE':
            return Favorite.objects.get(recipe_id=self.kwargs['id'])


class ShoppingCartView(CreateDestroyModelMixin):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.shopping_cart

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        if self.request.method == 'DELETE':
            return ShoppingCart.objects.get(recipe_id=self.kwargs['id'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="shopping_cart.csv"'
        },
    )
    writer = csv.writer(response)
    shopping_carts = request.user.shopping_cart.all()
    output_data = {}
    for cart in shopping_carts:
        ingredients = cart.recipe.ingredients.all()
        for ingredient in ingredients:
            data = IngrRecipeSerializerGet(ingredient).data
            if data['name'] in output_data.keys():
                output_data[data['name']]['amount'] += data['amount']
            else:
                output_data[data['name']] = {
                    'amount': data['amount'],
                    'measurement_unit': data['measurement_unit']
                }
    for data in output_data:
        writer.writerow((
            data, output_data[data]['amount'],
            output_data[data]['measurement_unit'])
        )

    return response
