from django import forms
from .models import Mission
from django_ckeditor_5.widgets import CKEditor5Widget

class MissionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["body"].required = False

    class Meta:
        model = Mission
        fields = ('title', 'body')
        widgets = {
            'body': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
