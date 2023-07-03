import datetime

from django import forms
from django.contrib.auth.models import User
from .models import Profile, Keywork, Task


class UserLoginForm(forms.Form):
   username = forms.CharField()
   password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
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
   avatar = forms.ImageField(widget=forms.FileInput)
   class Meta:
      model = Profile
      fields = ('phone', 'avatar', 'bio', 'department', 'team', 'team_leader')

class DepartmentTeamForm(forms.ModelForm):
   DEPARTMENT_CHOICES = [
      ('业务运营与IT支撑中心', '业务运营与IT支撑中心'),
   ]

   TEAM_CHOICES = [
      ('数据支撑班', '数据支撑班'),
      ('结算账务班', '结算账务班'),
      ('业务稽核班', '业务稽核班'),
      ('能力保障班', '能力保障班'),
      ('响应支撑班', '响应支撑班'),
      ('集中受理班', '集中受理班'),
      ('业务运营与IT支撑中心本部', '业务运营与IT支撑中心本部'),
   ]

   department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
   team = forms.ChoiceField(choices=TEAM_CHOICES)

   class Meta:
      model = Profile
      fields = ('department', 'team')


class KeyworkFilterForm(forms.Form):
   YEAR_CHOICES = [(r, r) for r in range(datetime.datetime.now().year, 2000, -1)]
   MONTH_CHOICES = [(r, r) for r in range(1, 13)]

   year = forms.ChoiceField(choices=YEAR_CHOICES)
   month = forms.ChoiceField(choices=MONTH_CHOICES)
   team = forms.ChoiceField(choices=DepartmentTeamForm.TEAM_CHOICES)




class TaskForm(forms.ModelForm):
   class Meta:
      model = Task
      fields = ['task', 'standard', 'score', 'completion']