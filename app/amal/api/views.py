from rest_framework import viewsets

from app.amal.api.serializers import AyahGroupSerializer, AyahSerializer
from app.amal.models import AyahGroup, Ayah


class AyahGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AyahGroup.objects.all().order_by('id')
    serializer_class = AyahGroupSerializer


class AyahViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayah.objects.filter(visible=True).order_by('id')
    serializer_class = AyahSerializer
