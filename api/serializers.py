from rest_framework import serializers
from api.models import Principle, Action, Cooperative, Period


class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = "__all__"


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
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
