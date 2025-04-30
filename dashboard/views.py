from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from questionnaire.models import Result, Answer, Question  # Import Question model
from django.db.models import Avg, Count
from django.db.models import Q  # Import Q object

@login_required
def dashboard_view(request):
    user = request.user

    # Último resultado do usuário
    ultimo_resultado = Result.objects.filter(user=user).order_by('-created_at').first()
    pontuacao_individual = ultimo_resultado.total_score if ultimo_resultado else 0

    # Classificação
    def classificar(pontos):
        if pontos == 0:
            return "Nenhum sofrimento mental identificado"
        elif 1 <= pontos <= 7:
            return "Sofrimento mental leve"
        elif 8 <= pontos <= 14:
            return "Sofrimento mental moderado"
        elif pontos >= 15:
            return "Sofrimento mental grave"
        return "Sem dados"

    classificacao = classificar(pontuacao_individual)

    # Métricas gerais
    resultados = Result.objects.all()
    total_usuarios = resultados.values('user').distinct().count()

    media_geral = resultados.aggregate(avg=Avg('total_score'))['avg'] or 0

    usuarios_com_transtorno = resultados.filter(total_score__gte=8).values('user').distinct().count()
    percentual_transtorno = (usuarios_com_transtorno / total_usuarios) * 100 if total_usuarios > 0 else 0

    # Histórico de respostas
    historico = Answer.objects.filter(user=user).order_by('-created_at')

    # Dados para o gráfico de distribuição de respostas
    resposta_distribuicao = []
    for pergunta in Question.objects.all():
        sim_respostas = Answer.objects.filter(user=user, question=pergunta, resposta=True).count()
        nao_respostas = Answer.objects.filter(user=user, question=pergunta, resposta=False).count()
        resposta_distribuicao.append({
            'pergunta': pergunta.texto,
            'sim': sim_respostas,
            'nao': nao_respostas,
        })

    context = {
        'pontuacao': pontuacao_individual,
        'classificacao': classificacao,
        'media_geral': round(media_geral, 2),
        'percentual_transtorno': round(percentual_transtorno, 2),
        'historico': historico,
        'resposta_distribuicao': resposta_distribuicao,  # Adiciona os dados para o gráfico
    }

    return render(request, 'dashboard/dashboard.html', context)