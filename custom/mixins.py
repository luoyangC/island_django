"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from rest_framework import status
from rest_framework import mixins

from custom.response import JsonResponse


class CreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, headers=headers)


class ListModelMixin(mixins.ListModelMixin):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


class UpdateModelMixin(mixins.UpdateModelMixin):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


class DestroyModelMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=None, status=status.HTTP_200_OK)
