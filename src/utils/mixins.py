from rest_framework import mixins
from utils import responses
from utils.decorators import handle_404, handle_permission_denied, handle_parameter_missing
from rest_framework import status


class CreateModelMixin(mixins.RetrieveModelMixin):
    @handle_permission_denied
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return responses.successful_response(serializer.data, status.HTTP_201_CREATED, headers)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    @handle_404
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return responses.successful_response(serializer.data)


class ListModelMixin(mixins.ListModelMixin):
    @handle_parameter_missing
    @handle_permission_denied
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return responses.successful_response(serializer.data)


class DestroyModelMixin(mixins.DestroyModelMixin):
    @handle_permission_denied
    @handle_404
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.successful_response()

    def perform_destroy(self, instance):
        instance.deactivate()


class UpdateModelMixin(mixins.UpdateModelMixin):
    @handle_permission_denied
    @handle_404
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.successful_response(serializer.data)
