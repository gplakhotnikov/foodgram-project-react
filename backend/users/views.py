from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import SubscriptionSerializer
from users.serializers import SubscriptionValidateSerializer

from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path='subscriptions',
            url_name='subscriptions', permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=('post', 'delete'), detail=True, url_path='subscribe',
            url_name='subscribe', permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        subscription = Subscription.objects.filter(
            author=author, user=user)
        if request.method == 'POST':
            data = {
                'user': user.id,
                'author': author.id}
            serializer = SubscriptionValidateSerializer(
                data=data,
                context={'request': request})
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscription.objects.create(author=author, user=user)
            serializer = SubscriptionSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'errors': 'Вы уже отписались от этого автора'},
                    status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
