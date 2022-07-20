from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteView, IngredientsViewSet, RecipesViewSet,
                    ShoppingCartView, SubscribesListView, SubscribesView,
                    TagsViewSet, download_shopping_cart)

router = routers.DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribesListView.as_view({
            'get': 'list'
        }
        ),
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribesView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribes'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shoping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='shopping_cart'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
