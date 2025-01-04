from rest_framework import serializers

from app.amal.models import AyahGroup, Ayah


class AyahGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyahGroup
        fields = ['id', 'title', 'subtitle', ]
        read_only_fields = ['id', 'title', 'subtitle', ]


class AyahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayah
        fields = ['id', 'group', 'title', 'position', 'arabic', 'indopak', 'bangla', 'ref', 'audiopath']
        read_only_fields = ['id', 'group', 'title', 'position', 'arabic', 'indopak', 'bangla', 'ref', 'audiopath']
