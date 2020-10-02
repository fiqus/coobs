from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext as _
from api.serializers import CooperativeSerializer
from api.models import Principle, Action, Period, Cooperative, Partner

def make_coop_active(self, request, cooperative):
  coop_serializer = CooperativeSerializer(cooperative, {'is_active': True}, partial=True)
  if not coop_serializer.is_valid(raise_exception=True):
    return False
  coop_serializer.save()
  return True


def send_email_activated_user_and_coop(partner):
  public_url = "{}://{}".format(settings.WEB_PROTOCOL, settings.WEB_URL)
  context = {'public_url': public_url, 'email': partner.email}
  text_template = get_template('coop_activated_email_template.txt')
  text_content = text_template.render(context)
  html_template = get_template('coop_activated_email_template.html')
  html_content = html_template.render(context)
  subject = _('Hello %(partner_name)s, your cooperative is been added to COOBS!') % {"partner_name": partner.first_name}
  email = EmailMultiAlternatives(subject, text_content,
                                  getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
                                  [partner.email])
  email.content_subtype = "html"
  email.attach_alternative(html_content, "text/html")
  email.send()

class PartnerAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'cooperative', 'is_active']
    actions = ['make_active']
    list_filter = ['cooperative', 'is_active']

    def make_active(self, request, queryset):
      if len(queryset)>1:
        self.message_user(request, ngettext(
            'select just one user to mark as active.',
            'select just one user to mark as active.',
            len(queryset),
        ), messages.ERROR)
      else:
        cooperative = queryset[0].cooperative
        coop_updated = make_coop_active(self, request, cooperative)
        if not coop_updated:
          self.message_user(request, ngettext(
              'The cooperative associated to the selected user is not valid.',
              'The cooperative associated to the selected user is not valid.',
              len(queryset),
          ), messages.ERROR)
        else:
          updated = queryset.update(is_active=True)
          send_email_activated_user_and_coop(queryset[0])

          self.message_user(request, ngettext(
              '%d user was successfully marked as active.',
              '%d user was successfully marked as active.',
              updated,
          ) % updated, messages.SUCCESS)
    make_active.short_description = "Mark selected user as Active (just one)"

class ActionAdmin(admin.ModelAdmin):
    list_display = ['date', 'cooperative', 'name', 'invested_money', 'invested_hours', 'public']
    list_filter = ['cooperative', 'date']

class CooperativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_name', 'starting_date', 'is_active']
    list_filter = ['name', 'is_active']

class PrincipleAdmin(admin.ModelAdmin):
    list_display = ['main_principle', 'cooperative', 'visible']
    list_filter = ['cooperative', 'visible']

admin.site.register(Principle, PrincipleAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Period)
admin.site.register(Cooperative, CooperativeAdmin)
admin.site.register(Partner, PartnerAdmin)
