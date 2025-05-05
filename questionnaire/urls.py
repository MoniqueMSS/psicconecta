from django.urls import path
from . import views

urlpatterns = [
    path('', views.srq20_questionnaire, name='questionnaire_home'), 
    path('srq20/', views.srq20_questionnaire, name='srq20'),
    path('resultado/', views.resultado_view, name='resultado'),
]