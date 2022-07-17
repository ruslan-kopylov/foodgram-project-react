from re import A
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import Subscribe, User
from recipes.models import Tag, Ingredient, Recipe, RecipeIngr

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
    
    def get_is_subscribed(self, obj):
        id = self.context['request'].user.id
        if Subscribe.objects.filter(subscriber=id).filter(author=obj):
            return True
        return False 


class UserSerializerReadOnly(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = fields


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        data['user'] = user
        return data

class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('author', 'subscriber')
        read_only_fields = fields

    def to_representation(self, instance):
        serializer = UserSerializerReadOnly(instance.author, context=self.context)
        return serializer.data
    
    def validate(self, data):
        user = self.context['request'].user
        author_id = self.context['view'].kwargs['id']
        if user.id == author_id:
            raise serializers.ValidationError("Нельзя подписываться на себя")
        if Subscribe.objects.filter(author_id=author_id, subscriber=user):
            raise serializers.ValidationError("Вы уже подписаны на этого автора")
        return data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngrRecipeSerializerGet(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngr
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_name(self, obj):
        return obj.ingredient.name
    
    def get_id(self, obj):
        return obj.ingredient.id


class IngrRecipeSerializerPost(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = RecipeIngr
        fields = ('id', 'amount')


class RecipeSerializerGet(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngrRecipeSerializerGet(many=True)
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            #'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )
        

class RecipeSerializerPost(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngrRecipeSerializerPost(many=True)
    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            #'is_favorited', 'is_in_shopping_cart',
            'image', 'name', 'text', 'cooking_time'
        )


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngr.objects.create(ingredient=ingredient, recipe=recipe, amount=amount)
        return recipe

    def to_representation(self, instance):
        serializer = RecipeSerializerGet(instance, context=self.context)
        return serializer.data 