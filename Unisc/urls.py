from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.authtoken import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('questionnaire/', include('questionnaire.urls')),

    # URLs do Simple JWT
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # URL para obter o token de autenticação básica do DRF (mantenha esta)
    path('api-token-auth/', views.obtain_auth_token),

    path('', lambda request: redirect('login', permanent=False)),
]