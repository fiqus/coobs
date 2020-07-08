"""coobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from django.conf.urls import url
from api.views import PrincipleView, ActionView, PeriodView, CooperativeView, PartnerView, \
    MyTokenObtainPairView, DashboardView, BalanceView, ActionsRankingView, PartnerStatsView, \
         SustainableDevelopmentGoalView, SDGBalanceView, SDGObjectiveView, SDGMonitoringView, \
             PublicActionView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)
from rest_framework.documentation import include_docs_urls


router = routers.DefaultRouter()
router.register(r'cooperatives', CooperativeView)
router.register(r'principles', PrincipleView, basename="Principle")
router.register(r'actions', ActionView, basename="Action")
router.register(r'periods', PeriodView, basename="Period")
router.register(r'partners', PartnerView, basename="Partner")
router.register(r'dashboard', DashboardView, basename="Dashboard")
router.register(r'balance', BalanceView, basename="Balance")
router.register(r'sdg-balance', SDGBalanceView, basename="BalanceODS")
router.register(r'actions-ranking', ActionsRankingView, basename="ActionsRanking")
router.register(r'my-stats', PartnerStatsView, basename="PartnerStats")
router.register(r'sustainable-development-goals', SustainableDevelopmentGoalView, basename="SustainableDevelopmentGoal")
router.register(r'sdg-objectives', SDGObjectiveView, basename="SDGObjective")
router.register(r'sdg-monitoring', SDGMonitoringView, basename="SDGMonitoring")

urlpatterns = [
    path('', RedirectView.as_view(url='api/')),
    path('docs/', include_docs_urls(title='COOBS API', permission_classes=[], public=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/public-actions', PublicActionView.as_view(), name='public_actions'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    url(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
