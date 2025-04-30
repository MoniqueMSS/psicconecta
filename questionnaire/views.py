from django.shortcuts import render, redirect
from .models import Question, Answer, Result
from .forms import SRQ20Form
from django.contrib.auth.decorators import login_required

@login_required
def srq20_questionnaire(request):
    if request.method == 'POST':
        form = SRQ20Form(request.POST)
        if form.is_valid():
            user = request.user
            total_score = 0

            # Limpa respostas anteriores (opcional)
            Answer.objects.filter(user=user).delete()

            for key, value in form.cleaned_data.items():
                question_id = int(key.split('_')[1])
                question = Question.objects.get(id=question_id)

                Answer.objects.create(
                    user=user,
                    question=question,
                    resposta=bool(int(value))  # Sim = 1, Não = 0
                )

                total_score += int(value)

            # Salva o total
            Result.objects.create(
                user=user,
                total_score=total_score
            )

            return redirect('resultado')
    else:
        form = SRQ20Form()

    return render(request, 'questionnaire/srq20.html', {'form': form})

@login_required
def resultado_view(request):
    try:
        resultado = Result.objects.filter(user=request.user).latest('created_at')
    except Result.DoesNotExist:
        resultado = None

    classificacao = None
    if resultado:
        if resultado.total_score == 0:
            classificacao = "Nenhum sofrimento mental identificado."
        elif 1 <= resultado.total_score <= 7:
            classificacao = "Sofrimento mental leve."
        elif 8 <= resultado.total_score <= 14:
            classificacao = "Sofrimento mental moderado."
        elif 15 <= resultado.total_score <= 20:
            classificacao = "Sofrimento mental grave."

    return render(request, 'questionnaire/resultado.html', {
        'resultado': resultado,
        'classificacao': classificacao
    })
