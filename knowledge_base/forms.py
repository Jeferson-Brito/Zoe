from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'visibility']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'})
        }

from .models import LearnedKnowledge

class LearnedKnowledgeForm(forms.ModelForm):
    class Meta:
        model = LearnedKnowledge
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
