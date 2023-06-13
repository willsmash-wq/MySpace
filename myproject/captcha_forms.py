from django import forms
from captcha.fields import CaptchaField
class Captcha(forms.Form):
    captcha = CaptchaField(required=True, error_messages={
        'invalid': '验证码输入错误'
    })