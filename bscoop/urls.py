"""bscoop URL Configuration

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
from api.views import PrincipleView, ActionView, PeriodView, CooperativeView, PartnerView, PartnerCreateView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'principles', PrincipleView)
router.register(r'actions', ActionView)
router.register(r'periods', PeriodView)
router.register(r'cooperatives', CooperativeView)
router.register(r'partners', PartnerView)
router.register(r'partner/create', PartnerCreateView)

urlpatterns = [
    path('', RedirectView.as_view(url='api/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/api-token-auth/', obtain_jwt_token),
    path('api/api-token-refresh/', refresh_jwt_token),
    path('api/api-token-verify/', verify_jwt_token)
]
