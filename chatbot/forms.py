# forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }
