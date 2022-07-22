from rest_framework import mixins, viewsets


class CreateDestroyModelMixin(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass
