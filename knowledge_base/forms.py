from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'filename', 'visibility']
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Documento'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'})
        }
