from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.fields import Hex2NameColor
from recipes.models import (FavoriteRecipeUser, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCartUser, Tag)
from users.models import Subscriptions

User = get_user_model()


class SubRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return user_is_subscribed(self, obj)

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        interest_user = obj
        if recipes_limit:
            return SubRecipeSerializer(
                Recipe.objects.filter(author=interest_user)
                [:int(recipes_limit)], many=True).data
        return SubRecipeSerializer(
            Recipe.objects.filter(author=interest_user), many=True).data


def user_is_subscribed(self, obj):
    user = self.context['request'].user
    if user.is_anonymous:
        return False
    return Subscriptions.objects.filter(user=user, following=obj.pk).exists()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return user_is_subscribed(self, obj)


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def validate_password(self, value):
        return make_password(value)


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='ingredient_in_recipe'
    )
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
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if (user != AnonymousUser()
                and FavoriteRecipeUser.objects.filter(
                    user=user, recipe=obj.pk).exists()):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if (user != AnonymousUser()
                and ShoppingCartUser.objects.filter(
                    user=user, recipe=obj.pk).exists()):
            return True
        return False


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо выбрать ингредиенты!')
        for ingredient in ingredients:
            cur_id = ingredient['id']
            current_ingredient = Ingredient.objects.filter(id=cur_id).first()
            if not current_ingredient:
                raise serializers.ValidationError(
                    f'Недопустимый id ингредиента \"{cur_id}\" -'
                    + 'ингредиент не существует.')
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1!')
        ids = [ingredient['id'] for ingredient in ingredients]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                'Данный ингредиент уже есть в рецепте!')
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Необходимо выбрать теги!')
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Теги должны быть уникальными!')
        return tags

    def add_ingredients_and_tags(self, tags, ingredients, recipe):
        recipe.tags.set(tags)
        ingredients_list = []
        for ingredient in ingredients:
            new_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )
            ingredients_list.append(new_ingredient)
        RecipeIngredient.objects.bulk_create(ingredients_list)
        return recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self.add_ingredients_and_tags(tags, ingredients, recipe)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        return self.add_ingredients_and_tags(
            tags, ingredients, instance
        )
