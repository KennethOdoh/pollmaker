from django import forms
from .models import Question, Choice
class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text',
        ]

class CreateChoice(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            'choice_text'
        ]

