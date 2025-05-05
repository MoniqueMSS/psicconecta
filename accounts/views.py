from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, SetNewPasswordForm  # Import SetNewPasswordForm
from django.http import JsonResponse
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import AuthenticationForm  # Import AuthenticationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm # Importe o PasswordResetForm
from django.contrib.auth.models import User

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # redireciona para o dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Gerar tokens JWT para o usuário logado
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Definindo os tokens como cookies HTTP-only
                response = redirect('dashboard')  # Redirecionar para o dashboard
                response.set_cookie('access_token', access_token, httponly=True)
                response.set_cookie('refresh_token', refresh_token, httponly=True)
                return response
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Assume que os dados estão em JSON
            form = CustomUserCreationForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse({'message': 'Usuário registrado com sucesso!'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Por favor, envie dados em formato JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido. Use POST para registrar.'}, status=405)

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST) # Instancia o formulário com os dados do POST
        if form.is_valid():
            email = form.cleaned_data['email'] # Obtém o email validado do formulário
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Enviar e-mail
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            )
            subject = "Redefinição de Senha"
            message = f"Olá, aqui está o link para redefinir sua senha: {reset_url}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            return render(request, 'accounts/password_reset_done.html')
        else:
             return render(request, 'accounts/password_reset_request.html', {'form': form, 'error': 'Email não encontrado'})
    else:
        form = PasswordResetForm() # Instancia o formulário vazio para exibir na página inicial
    return render(request, 'accounts/password_reset_request.html', {'form': form}) # Passe o formulário para o template

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                return render(request, 'accounts/password_reset_complete.html')  # Criar este template
        else:
            form = SetNewPasswordForm()
            return render(request, 'accounts/password_reset_form.html', {'form': form})  # Criar este template
    else:
        return render(request, 'accounts/password_reset_invalid.html')  # Criar este template