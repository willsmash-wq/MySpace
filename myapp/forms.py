from django import forms
from .models import Mission

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ('title', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
