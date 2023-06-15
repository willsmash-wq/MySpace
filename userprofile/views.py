from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from userprofile.forms import UserLoginForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from userprofile.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("myapp:mission_list")
            else:
                return HttpResponse("账号或密码输入有误,请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == "GET":
        if request.user.is_authenticated:  # 用户已经登录
            return redirect('myapp:mission_list')  # 重定向到list页面
        else:
            user_login_form = UserLoginForm()
            context = {'from': user_login_form}
            return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

def user_logout(request):
        logout(request)
        response = redirect(reverse('userprofile:login'))
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')
        return response


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("myapp:mission_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

def registered_users(request):
    users = User.objects.values('username')  # 获取所有用户的用户名
    user_list = list(users)  # 转换为Python list
    print(user_list)  # 打印用户列表
    return JsonResponse({'users': user_list}, safe=False)


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect("myapp:mission_list")
    else:
        return HttpResponse("你没有删除操作的权限。")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id是OneToOneField自动生成的字段
    profile = Profile.objects.get(user_id=id)

    if request.method == 'POST':
        # 验证修改数据者是否为本人
        if request.user != user:
            return HttpResponse("你没有权限修改次用户信息")

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cleaned_data = profile_form.cleaned_data
            profile.phone = profile_cleaned_data['phone']
            profile.bio = profile_cleaned_data['bio']
            profile.save()
            return redirect("userprofile:edit", id=id)

        else:
            return HttpResponse("注册表单输入有误,请重新输入")

    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")