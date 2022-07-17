from django.urls import include, path
from rest_framework import routers

from .views import (SubscribesListView, UsersViewSet, Logout, ObtainAuthToken, TagsViewSet,
                    IngredientsViewSet, RecipesViewSet, SubscribesView)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        SubscribesView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribes'
    ),
    path(
        'users/subscriptions/',
        SubscribesListView.as_view({
            'get': 'list'
        }
        ),
        name='subscriptions'
    ),
    path('', include(router.urls)),
    path(
        'auth/token/login/',
        ObtainAuthToken.as_view(),
        name='api_auth_token',
    ),
    path(
        'auth/token/logout/',
        Logout.as_view(),
        name='api_logout',
    ),  
#    path(
#        'users/<int:id>/subscribe/',
#        SubscribesView.as_view({'post': 'create'}),
#        name='subscribes'
#    ),
]

