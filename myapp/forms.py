from django import forms
from .models import Mission

class MissionForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Mission
        fields = ('title', 'body', 'image')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
