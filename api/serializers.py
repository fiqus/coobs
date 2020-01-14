from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Principle, Action, Period, Cooperative, Partner
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_rest_framework_camel_case.util import camelize
from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class PrincipleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='main_principle.name', read_only=True)
    name_key = serializers.CharField(source='main_principle.name_key', read_only=True)

    class Meta:
        model = Principle
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    principle_name_key = serializers.CharField(source='principle', read_only=True)

    class Meta:
        model = Action
        fields = "__all__"


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = "__all__"

    def validate_date_from(self, value):
        id = self.instance.id if self.instance is not None else None
        cooperative_id = self.initial_data['cooperative']  if self.initial_data.get('cooperative') is not None else self.initial_data['cooperative_id']
        periods = Period.get_date_period(id, value, cooperative_id)
        if periods.count() > 0:
            raise serializers.ValidationError(_("The date from you entered is contained in another period."))
        return value

    def validate_date_to(self, value):
        id = self.instance.id if self.instance is not None else None
        cooperative_id = self.initial_data['cooperative']  if self.initial_data.get('cooperative') is not None else self.initial_data['cooperative_id']
        periods = Period.get_date_period(id, value, cooperative_id)
        if periods.count() > 0:
            raise serializers.ValidationError(_("The date to you entered is contained in another period."))
        return value

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = "__all__"

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cooperative_id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': [UnicodeUsernameValidator()]}
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if self.initial_data.get('new_password'):
            password_change_data = {'new_password': self.initial_data.get('new_password'), 'confirm_password': self.initial_data.get('confirm_password')}
            change_pass_serializer = ChangePasswordSerializer(data=password_change_data)
            change_pass_serializer.is_valid(raise_exception=True)
            instance.set_password(self.initial_data.get('new_password'))

        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField("^(?=.*[a-zA-Z])(?=.*[0-9])", min_length=8, error_messages={'invalid': 'Password must be more than 8 characters long, contain letters and numbers'})
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match")
        return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        data = get_object_or_404(Cooperative, pk=user.cooperative_id)
        coop_data = CooperativeSerializer(data).data

        user_data = PartnerSerializer(user).data
        token['user'] = camelize(user_data)
        token['cooperative'] = camelize(coop_data)

        return token
