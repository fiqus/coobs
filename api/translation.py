from modeltranslation.translator import register, TranslationOptions
from api.models import MainPrinciple, SustainableDevelopmentGoal

@register(MainPrinciple)
class MainPrincipleTranslationOptions(TranslationOptions):
    fields = ('description',)
    
@register(SustainableDevelopmentGoal)
class SustainableDevelopmentGoalTranslationOptions(TranslationOptions):
    fields = ('name', 'description')