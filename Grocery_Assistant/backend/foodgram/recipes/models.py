from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField, CheckConstraint, Q, UniqueConstraint
from django.db.models.functions import Length

from recipes.validators import hex_field_validator

User = get_user_model()
CharField.register_lookup(Length)


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Тег',
        help_text='Введите название',
    )
    color = ColorField(
        format='hex',
        default='#FF0000',
        verbose_name='Цвет в HEX',
        help_text='Цветовой HEX-код',
        validators=[hex_field_validator])

    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Уникальный слаг',
        help_text='Введите слаг для тега',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_name_unit_unique'
            ),
            CheckConstraint(
                check=Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
            CheckConstraint(
                check=Q(measurement_unit__length__gt=0),
                name="\n%(app_label)s_%(class)s_measurement_unit is empty\n",
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        through='RecipeTag',
        verbose_name='Список тегов',
        help_text='Список тегов',
        related_name='tags_recipes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Автор рецепта',
        related_name='author_recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        help_text='Ингредиенты для приготовления блюда',
        related_name='ingredients_recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        verbose_name='Ссылка на картинку',
        help_text='Загрузите ссылку на картинку к рецепту',
        upload_to='recipes',
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Время приготовления должно быть не менее 1 минуты!'
        )]
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            UniqueConstraint(
                fields=("name", "author"),
                name="unique_for_author",
            ),
            CheckConstraint(
                check=Q(name__length__gt=0),
                name="\n%(app_label)s_%(class)s_name is empty\n",
            ),
        )

    def __str__(self):
        return self.name[:15]

    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Рецепты_Тег'
        verbose_name_plural = 'Рецепты_Тег'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag_unique'
            )
        ]

    def __str__(self):
        return f'У рецепта {self.recipe} есть тег {self.tag}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Рецепт',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента в рецепте',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество должно быть больше 0.'
            ),
        ],
    )

    class Meta:
        verbose_name = 'Рецепт_Ингредиенты'
        verbose_name_plural = 'Рецепт_Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='\n%(app_label)s_%(class)s ingredient alredy added\n'
            )
        ]

    def __str__(self):
        return f'В рецепте {self.recipe} есть ингредиент {self.ingredient}'


class ShoppingCartUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_in_shoplist',
        verbose_name='Пользователь, имеющий рецепт в cписке покупок',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_shoplist',
        verbose_name='Рецепт из списка покупок пользователя',
        help_text='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='\n%(app_label)s_%(class)s recipe is cart alredy\n',
            ),
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'


class FavoriteRecipeUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь, имеющий избранные рецепты',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранный рецепт определенного пользователя',
        help_text='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='\n%(app_label)s_%(class)s recipe is favorite alredy\n'
            ),
        ]
