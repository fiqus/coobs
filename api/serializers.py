from rest_framework import serializers
from api.models import Principle, Action, Period


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    principle_name = serializers.CharField(source='principle', read_only=True)

    class Meta:
        model = Action
        fields = "__all__"


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"

    @staticmethod
    def validate_date_from(value):
        periods = Period.get_date_period(value)
        if periods.count() > 0:
            raise serializers.ValidationError("The date from you entered is contained in another period.")
        return value

    @staticmethod
    def validate_date_to(value):
        periods = Period.get_date_period(value)
        if periods.count() > 0:
            raise serializers.ValidationError("The date to you entered is contained in another period.")
        return value
