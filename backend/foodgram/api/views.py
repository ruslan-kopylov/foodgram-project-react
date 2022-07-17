from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import AuthenticatedForObject, AuthorOrReadOnly
from .serializers import (TagSerializer, UserSerializer,
                          AuthTokenSerializer, PasswordSerializer,
                          SubscribeSerializer,
                          IngredientSerializer, RecipeSerializerGet,
                          RecipeSerializerPost)
from users.models import User, Subscribe
from recipes.models import Tag, Ingredient, Recipe


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ObtainAuthToken(APIView):
    serializer_class = AuthTokenSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthenticatedForObject]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    @action(methods=['post'], detail=False, url_path='set_password')
    def set_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get('current_password')
            try:
                email = request.user.email
                user = authenticate(password=password, email=email)
                user.password = serializer.data.get('new_password')
                user.save()
                return Response({'status': 'password set'}, status=status.HTTP_200_OK)
            except:
                return Response({'detail': 'Учетные данные не были предоставлены.'}, 
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False, url_path='me')
    def me(self, request):
        if request.user:
            serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination

class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',) 
    pagination_class = LimitOffsetPagination

class RecipesViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination

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
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(author__subscriber=self.request.user)

class SubscribesView(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        author = User.objects.get(id=self.kwargs['id'])
        serializer.save(author=author, subscriber=self.request.user)

    def get_object(self):
        if self.request.method == 'POST':
            return User.objects.get(id=self.kwargs['id'])
        if self.request.method == 'DELETE':
            return Subscribe.objects.get(author_id=self.kwargs['id'])



