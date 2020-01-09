from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import datetime


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

    def __str__(self):
        return self.name

class Principle(models.Model):
    description = models.TextField(_('description'))
    visible = models.BooleanField(default=True)
    main_principle = models.ForeignKey(MainPrinciple, on_delete=models.CASCADE, null=True, verbose_name=_('main principle'))
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))

    class Meta:
        verbose_name = _('principle')

    def __str__(self):
        return self.main_principle.name

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

    @staticmethod
    def get_date_period(pk, date, cooperative_id):
        qs = Period.objects.filter(cooperative__id=cooperative_id, date_from__lte=date, date_to__gte=date)
        if pk is not None:
            qs = qs.exclude(pk=pk)
        return qs

    def get_current(self):
        today = datetime.date.today()
        # Note that if there are two periods that overlap, it returns the last one.
        return self.get_date_period(today).last()


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
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE, null=True, verbose_name=_('principle'))
    date = models.DateField(_('date'), default=datetime.date.today)
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), null=True, blank=True)
    invested_money = models.DecimalField(_('invested money'), max_digits=19, decimal_places=2, null=True)
    partners_involved = models.ManyToManyField(Partner, verbose_name=_('partners involved'))
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, blank=False, null=True, verbose_name=_('cooperative'))

    class Meta:
        verbose_name = _('action')

    def __str__(self):
        return '%s - %s ' % (self.date, self.principle)