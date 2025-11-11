from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'created_at': forms.TextInput(attrs={'readonly': 'readonly'}),
            'update_at': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

