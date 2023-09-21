from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class ListCreateViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    pass
