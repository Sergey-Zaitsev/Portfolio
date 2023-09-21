from django.contrib import admin
from django.contrib.admin import display

from .models import (FavoriteRecipeUser, Ingredient, Recipe, RecipeIngredient,
                     RecipeTag, ShoppingCartUser, Tag)


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 0


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'favorite_recipes',
                    'cooking_time', 'pub_date')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientsInLine, TagInLine)

    @display(description='Количество в избранных')
    def favorite_recipes(self, obj):
        return FavoriteRecipeUser.objects.filter(recipe=obj).count()

    class Meta:
        model = Recipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)


@admin.register(ShoppingCartUser)
class ShoppingCartUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(FavoriteRecipeUser)
class FavoriteRecipeUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
