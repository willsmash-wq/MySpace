from django import forms
from django.contrib.auth.models import User
from .models import Profile
class UserLoginForm(forms.Form):
   username = forms.CharField()
   password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
   # 复写 User 的密码
   password = forms.CharField()
   password2 = forms.CharField()

   class Meta:
      model = User
      fields = ('username', 'email', 'password')

   def clean_password2(self):
      data = self.cleaned_data
      if data.get('password') == data.get('password2'):
         return data.get('password')
      else:
         raise forms.ValidationError("密码输入不一致,请重试。")


class ProfileForm(forms.ModelForm):
   avatar = forms.ImageField(widget=forms.FileInput)  # add this line
   class Meta:
      model = Profile
      fields = ('phone', 'avatar', 'bio', 'department', 'team')



class DepartmentTeamForm(forms.ModelForm):
   DEPARTMENT_CHOICES = [
      ('业务运营与IT支撑中心', '业务运营与IT支撑中心'),
   ]

   TEAM_CHOICES = [
      ('数据支撑班', '数据支撑班'),
      ('业务稽核班', '业务稽核班'),
   ]

   department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
   team = forms.ChoiceField(choices=TEAM_CHOICES)

   class Meta:
      model = Profile
      fields = ('department', 'team')

