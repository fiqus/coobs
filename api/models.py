from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from django.db.models import Count
import datetime
from decimal import Decimal

class Cooperative(models.Model):
    name = models.CharField(_('name'), max_length=128, blank=True)
    business_name = models.CharField(_('business name'), max_length=128, null=False, blank=False, unique=True)
    starting_date = models.DateField(_('starting date'), default=datetime.date.today)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    class Meta:
        verbose_name = _('cooperative')

    def __str__(self):
        return '%s' % (self.business_name)


class MainPrinciple(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name_key = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, default="")
    description_key = models.CharField(max_length=256)

    def __str__(self):
        return self.name_key


class Principle(models.Model):
    description = models.TextField(_('description'))
    visible = models.BooleanField(default=True)
    main_principle = models.ForeignKey(MainPrinciple, on_delete=models.CASCADE, null=True, verbose_name=_('main principle'))
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))

    class Meta:
        verbose_name = _('principle')

    def __str__(self):
        return self.main_principle.name_key


class Period(models.Model):
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    date_from = models.DateField(_('date from'), default=datetime.date.today)
    date_to = models.DateField(_('date to'), default=datetime.date.today)
    actions_budget = models.DecimalField(_('actions budget'), max_digits=19, decimal_places=2)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))

    class Meta:
        verbose_name = _('period')

    def __str__(self):
        return self.name

    @classmethod
    def get_date_period(cls, pk, date, cooperative_id):
        qs = cls.objects.filter(cooperative__id=cooperative_id, date_from__lte=date, date_to__gte=date)
        if pk is not None:
            qs = qs.exclude(pk=pk)
        return qs

    @classmethod
    def get_current(cls, cooperative_id):
        today = datetime.date.today()
        # Note that if there are two periods that overlap, it returns the last one.
        current_period = cls.get_date_period(None, today, cooperative_id).last()
        if (current_period):
            return current_period
        return None


class Partner(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('partner')

    def __str__(self):
        return '%s - %s' % (self.email, self.cooperative)


class Action(models.Model):
    principles = models.ManyToManyField(Principle, blank=False, verbose_name=_('principles'))
    date = models.DateField(_('date'), default=datetime.date.today)
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), null=True, blank=True)
    invested_money = models.DecimalField(_('invested money'), max_digits=19, decimal_places=2, default=Decimal('0.00'), blank=True)
    partners_involved = models.ManyToManyField(Partner, verbose_name=_('partners involved'), blank=False)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))
    public = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('action')

    def __str__(self):
        return '%s - %s ' % (self.date, self.name)
    
    @classmethod
    def get_current_actions(cls, cooperative, date_from, date_to):
        qs = cls.objects.filter(cooperative=cooperative, principles__visible=True, date__gte=date_from, date__lte=date_to).annotate(principles_num = Count('id'))
        return qs
