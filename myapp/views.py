from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from .forms import MissionForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mission
from django.core.paginator import Paginator
import markdown
# 视图函数
from django.contrib.auth.decorators import login_required

@login_required
def mission_list(request):
    show_guide = False
    # 检查用户的部门和班组信息
    department = request.user.profile.department
    group = request.user.profile.team  # 修改此处，使用team代替group
    # 如果部门或班组是虚拟的，那么将show_guide设为True
    if department == '虚拟部门' or group == '虚拟班组':  # 修改此处，将virtual_department和virtual_group改为中文
        show_guide = True

    if request.GET.get('order') == 'total_views':
        mission_list = Mission.objects.all().order_by('-total_views')
        order = 'total_views'
    elif request.GET.get('order') == 'newest':
        mission_list = Mission.objects.all().order_by('-created')
        order = 'newest'
    else:
        mission_list = Mission.objects.all()
        order = 'normal'

    search_keyword = request.GET.get('search')
    if search_keyword:
        mission_list = mission_list.filter(
            Q(title__icontains=search_keyword) | Q(body__icontains=search_keyword)
        ).distinct()

    paginator = Paginator(mission_list, 9)
    page = request.GET.get('page')
    missions = paginator.get_page(page)

    context = {'missions': missions, 'order': order, 'show_guide': show_guide}
    return render(request, 'mission/list.html', context)

# 文章详情
def mission_detail(request, id):
    mission = Mission.objects.get(id=id)
    mission.total_views += 1
    mission.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    mission.body = md.convert(mission.body)
    context = {'mission': mission, 'toc': md.toc}
    return render(request, 'mission/detail.html', context)



@login_required(login_url='/userprofile/login')
def mission_create(request):
   # 判断用户是否提交数据
   if request.method == "POST":
       mission_post_form = MissionForm(data=request.POST)
       if mission_post_form.is_valid():
           new_mission = mission_post_form.save(commit=False)
           new_mission.mission_taker = User.objects.get(id=request.user.id)
           new_mission.save()
           return redirect('myapp:mission_list')
       else:
           return HttpResponse("表单内容有误,请重新填写")

   else:
       mission_post_form = MissionForm()
       context = {'mission_post_form': mission_post_form}
       return render(request, 'Mission/create.html', context)



def mission_delete(request, id):
   mission = Mission.objects.get(id=id)
   mission.delete()
   return redirect('myapp:mission_list')

def mission_update(request, id):
   mission = Mission.objects.get(id=id)
   if request.method =="POST":
       Mission_post_form = MissionForm(data=request.POST)
       if Mission_post_form.is_valid():
           mission.title = request.POST['title']
           mission.body = request.POST['body']
           mission.save()
           return redirect("myapp:mission_detail", id=id)
       else:
           return HttpResponse("表单内容有误,请重新填写")
   else:
       Mission_post_form = MissionForm()
       context = { 'mission': mission, 'Mission_post_form': Mission_post_form}
       return render(request, 'Mission/update.html', context)

