from rest_framework import serializers
from api.models import Principle


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = ('name', 'description')
