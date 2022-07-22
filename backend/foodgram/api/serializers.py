from collections import OrderedDict

from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngr,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.models import CustomUser, Subscribe


class UserSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializerReadOnly(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        id = self.context['request'].user.id
        if Subscribe.objects.filter(subscriber=id).filter(author=obj):
            return True
        return False


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('author', 'subscriber')
        read_only_fields = fields

    def to_representation(self, instance):
        serializer = SubscriptionsSerializer(
            instance.author, context=self.context
        )
        return OrderedDict(serializer.data)

    def validate(self, data):
        user = self.context['request'].user
        author_id = self.context['view'].kwargs['id']
        if user.id == author_id:
            raise serializers.ValidationError("Нельзя подписываться на себя")
        if Subscribe.objects.filter(author_id=author_id, subscriber=user):
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора")
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
    author = UserSerializerReadOnly()
    tags = TagSerializer(many=True)
    ingredients = IngrRecipeSerializerGet(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context['request'].user.id, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(
            user=self.context['request'].user.id, recipe=obj).exists()


class RecipeSerializerPost(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngrRecipeSerializerPost(many=True)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'image', 'name', 'text', 'cooking_time'
        )

    def update(sefl, instance, validated_data):
        if 'tags' in validated_data:
            new_tags = validated_data.pop('tags')
            current_tags = [tag for tag in instance.tags.filter()]
            add = [tag for tag in new_tags if tag not in current_tags]
            delete = [tag for tag in current_tags if tag not in new_tags]
            for tag in delete:
                instance.tags.remove(tag)
            for tag in add:
                instance.tags.add(tag)
        if 'ingredients' in validated_data:
            new_ingredients = validated_data.pop('ingredients')
            current_ingredients = [
                ingredient for ingredient in instance.ingredients.filter()
            ]
            for ingredient in new_ingredients:
                if RecipeIngr.objects.filter(
                    ingredient_id=ingredient['id'], recipe=instance
                ):
                    obj = RecipeIngr.objects.get(
                        ingredient_id=ingredient['id'], recipe=instance
                    )
                    if ingredient['amount'] != obj.amount:
                        obj.amount = ingredient['amount']
                    obj.save()
                    current_ingredients.remove(obj)
                else:
                    RecipeIngr.objects.create(
                        ingredient_id=ingredient['id'],
                        recipe=instance,
                        amount=ingredient['amount']
                    )
            for ingredient in current_ingredients:
                ingredient.delete()
        for data in validated_data:
            setattr(instance, data, validated_data[data])
        instance.save()
        return instance

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngr.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount)
        return recipe

    def to_representation(self, instance):
        serializer = RecipeSerializerGet(instance, context=self.context)
        return serializer.data


class RecipeSerializerFavorite(RecipeSerializerGet):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name', 'image', 'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        read_only_fields = fields

    def to_representation(self, instance):
        serializer = RecipeSerializerFavorite(
            instance.recipe, context=self.context)
        return serializer.data

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.context['view'].kwargs['id']
        if Favorite.objects.filter(recipe_id=recipe, user=user):
            raise serializers.ValidationError(
                "Рецепт уже добавлен в избранное")
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        read_only_fields = fields

    def to_representation(self, instance):
        serializer = RecipeSerializerFavorite(
            instance.recipe, context=self.context)
        return serializer.data

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.context['view'].kwargs['id']
        if ShoppingCart.objects.filter(recipe_id=recipe, user=user):
            raise serializers.ValidationError("Рецепт уже добавлен в корзину")
        return data


class SubscriptionsSerializer(UserSerializerReadOnly):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = fields

    def get_recipes(self, obj):
        limit = int(self.context['request'].GET.get('recipes_limit', 6))
        return RecipeSerializerGet(
            instance=obj.recipes.all()[:limit],
            many=True, context=self.context).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
