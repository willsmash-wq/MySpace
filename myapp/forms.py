from django import forms
from .models import Mission, Comment
from django_ckeditor_5.widgets import CKEditor5Widget

class MissionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置body字段为非必需
        self.fields["body"].required = False

    class Meta:
        model = Mission
        fields = ('title', 'body', 'article_type')
        widgets = {
            'body': CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="extends")
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
