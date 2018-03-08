from rest_framework import mixins, views
from utils import responses
from django.http import Http404


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404 as err:
            return responses.failed_response(err.__str__())

        serializer = self.get_serializer(instance)
        return responses.successful_response(serializer.data)


class ListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return responses.successful_response(serializer.data)
