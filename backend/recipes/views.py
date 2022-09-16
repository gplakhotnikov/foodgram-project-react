from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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
                {'errors': f'Невозможно добавить рецепт повторно'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {'errors': f'Невозможно удалить рецепт повторно'},
                status=status.HTTP_400_BAD_REQUEST)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True, url_path='favorite',
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

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart',
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

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_cart(self, request):
        user = request.user
        filename = 'shopping_list.txt'
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        
        final_list = {}
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]

        text_list = ['Список покупок:\n']
        text_list += ['\n']
        text_list += [
            f'{key.capitalize()} '
            f'({value.get("measurement_unit")}) '
            f'{value.get("amount")}\n' for key, value in final_list.items()]
        text_list += ['\n']
        text_list += ['Сгенерировано приложением Foodgram']
        response = HttpResponse(text_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{filename}"')
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
