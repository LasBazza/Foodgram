from rest_framework import viewsets, mixins


class CreateListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    pass
