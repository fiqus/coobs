from modeltranslation.translator import register, TranslationOptions
from api.models import MainPrinciple

@register(MainPrinciple)
class MainPrincipleTranslationOptions(TranslationOptions):
    fields = ('description',)