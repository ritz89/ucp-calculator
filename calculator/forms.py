from django import forms
from .models import Actor, Transaction, UseCase

class UseCaseForm(forms.ModelForm):
    class Meta:
        model = UseCase
        fields = ['name', 'description', 'complexity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'complexity': forms.Select(attrs={'class': 'form-control'}, choices=UseCase.COMPLEXITY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_attrs = {'class': 'form-label'}


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'actor_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'actor_type': forms.Select(attrs={'class': 'form-control'}, choices=Actor.ACTOR_TYPE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_attrs = {'class': 'form-label'}

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'complexity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'complexity': forms.Select(attrs={'class': 'form-control'}, choices=Transaction.COMPLEXITY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_attrs = {'class': 'form-label'}
