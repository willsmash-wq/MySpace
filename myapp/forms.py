from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Mission

# 写文章表单类
class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ('title', 'body')
        widgets = {
            'body': CKEditorWidget(),
        }
