from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.filters import RecipeFilter, IngredientSearchFilter
from recipes.models import Favorite, Recipe, Cart, IngredientAmount
from recipes.models import Ingredient, Tag
from recipes.permissions import AuthorOrReadOnly
from recipes.serializers import RecipeSerializer, ShortRecipeSerializer
from recipes.serializers import IngredientSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            return Response(
                {'errors': f'Невозможно добавить рецепт {recipe} повторно'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {'errors': f'Невозможно удалить рецепт {recipe} повторно'},
                status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('post', 'delete'), detail=True, url_path='favorite',
            url_name='favorite')
    def favorite(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            name = 'избранное'
            return self.add(Favorite, user, pk, name)
        if request.method == 'DELETE':
            name = 'избранного'
            return self.delete_relation(Favorite, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('post', 'delete'), detail=True, url_path='shopping_cart',
            url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            name = 'список покупок'
            return self.add(Cart, user, pk, name)
        if request.method == 'DELETE':
            name = 'списка покупок'
            return self.delete_relation(Cart, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('get',), detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=user).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    Sum('amount', distinct=True))
        text_list = ['Список покупок:\n']
        text_list += ['\n']
        text_list += [
            f'{i.get("ingredient__name").capitalize()} '
            f'({i.get("ingredient__measurement_unit")}) - '
            f'{i.get("amount__sum")}\n' for i in list(ingredients)]
        text_list += ['\n']
        text_list += ['Сгенерировано приложением Foodgram']
        response = HttpResponse(
            text_list,
            content_type=settings.EXPORT_CONTENT_TYPE)
        response['Content-Disposition'] = (
            f'attachment; filename="{settings.EXPORT_FILE_NAME}"')
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
