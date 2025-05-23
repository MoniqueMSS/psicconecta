from django.contrib.auth import views as auth_views
from django.urls import path
from . import views  # Importe suas views

urlpatterns = [
    # URL de login
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # URLs de redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    # URL de cadastro
    path('signup/', views.signup_view, name='signup'),  # Mapeia a URL 'signup/' para a sua view signup_view

    # URL de logout
    path('logout/', views.logout_view, name='logout'),  # Adicione esta linha

    # Adicione aqui outras URLs relacionadas à sua app 'accounts' (perfil, etc.)
]