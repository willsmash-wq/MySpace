import datetime

from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from userprofile.forms import UserLoginForm, DepartmentTeamForm, KeyworkFilterForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from userprofile.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile, Keywork


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
    profile = Profile.objects.get(user_id=id)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("你没有权限修改次用户信息")

        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  # 注意这里添加了 request.FILES
        if profile_form.is_valid():
            profile_form.save()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误,请重新输入")

    elif request.method == "GET":
        profile_form = ProfileForm(instance=profile)  # 这里添加了 instance=profile，以便于显示原先的数据
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


from django.core.exceptions import PermissionDenied


@login_required
def keywork_view(request):
    year = request.GET.get('year', datetime.datetime.now().year)
    month = request.GET.get('month', datetime.datetime.now().month)
    team = request.GET.get('team', request.user.profile.team)

    form = KeyworkFilterForm(initial={'year': year, 'month': month, 'team': team})

    if request.method == 'POST':
        form = KeyworkFilterForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            team = form.cleaned_data['team']
            keywork, created = Keywork.objects.get_or_create(year=year, month=month, team=team,
                                                             defaults={'last_edit_by': request.user})
            if request.user.profile.team_leader and keywork.team == request.user.profile.team:
                keywork.content = request.POST.get('content')
                keywork.last_edit_by = request.user
                keywork.save()

    keywork, created = Keywork.objects.get_or_create(year=year, month=month, team=team,
                                                     defaults={'last_edit_by': request.user})

    return render(request, 'Mission/keywork.html', {'form': form, 'keywork': keywork})