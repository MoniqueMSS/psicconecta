from django.db import models
from django.conf import settings  # Importe settings
from django.utils import timezone


class Question(models.Model):
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    resposta = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)


class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    total_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)