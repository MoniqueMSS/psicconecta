from django import forms
from .models import Question

class SRQ20Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SRQ20Form, self).__init__(*args, **kwargs)
        
        # Pega todas as perguntas do banco
        questions = Question.objects.all()
        
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.texto,
                choices=[(1, 'Sim'), (0, 'Não')],
                widget=forms.RadioSelect,
                required=True
            )
