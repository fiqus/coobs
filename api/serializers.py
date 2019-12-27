from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Principle, Action, Period, Cooperative, Partner

User = get_user_model()

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

    def validate_date_from(self, value):
        id = self.instance.id if self.instance is not None else None
        periods = Period.get_date_period(id, value)
        if periods.count() > 0:
            raise serializers.ValidationError("The date from you entered is contained in another period.")
        return value

    def validate_date_to(self, value):
        id = self.instance.id if self.instance is not None else None
        periods = Period.get_date_period(id, value)
        if periods.count() > 0:
            raise serializers.ValidationError("The date to you entered is contained in another period.")
        return value

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = "__all__"
    
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'cooperative', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
