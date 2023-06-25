from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from userprofile.forms import DepartmentTeamForm
from .forms import MissionForm, CommentForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mission, Comment
from django.core.paginator import Paginator
from django.conf import settings
import markdown
# 视图函数
from django.contrib.auth.decorators import login_required

@login_required
def mission_list(request):
    show_guide = False
    # 检查用户的部门和班组信息
    department = request.user.profile.department
    team = request.user.profile.team
    # 如果部门或班组是虚拟的，那么将 show_guide 设为 True
    if department == '虚拟部门' or team == '虚拟班组':
        show_guide = True

    if request.method == 'POST':
        form = DepartmentTeamForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('myapp:mission_list')  # 重定向到 mission_list 视图
    else:
        form = DepartmentTeamForm(instance=request.user.profile)

    order = request.GET.get('order')
    if order == 'total_views':
        mission_list = Mission.objects.all().order_by('-total_views')
    elif order == 'newest':
        mission_list = Mission.objects.all().order_by('-created')
    else:
        mission_list = Mission.objects.all()

    search_keyword = request.GET.get('search')
    if search_keyword:
        mission_list = mission_list.filter(
            Q(title__icontains=search_keyword) | Q(body__icontains=search_keyword)
        ).distinct()

    category = request.GET.get('category')
    if category:
        mission_list = mission_list.filter(article_type=category)

    paginator = Paginator(mission_list, 9)
    page = request.GET.get('page')
    missions = paginator.get_page(page)

    context = {
        'missions': missions,
        'order': order,
        'show_guide': show_guide,
        'form': form,
        'selected_category': category,
    }
    return render(request, 'mission/list.html', context)

# 文章详情
def mission_detail(request, id):
    mission = Mission.objects.get(id=id)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.mission = mission
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

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
    context = {'mission': mission, 'toc': md.toc, 'comments': mission.comments.all(), 'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'mission/detail.html', context)



@login_required(login_url='/userprofile/login')
def mission_create(request):
    if request.method == "POST":
        mission_post_form = MissionForm(request.POST, request.FILES)
        if mission_post_form.is_valid():
            new_mission = mission_post_form.save(commit=False)
            new_mission.mission_taker = User.objects.get(id=request.user.id)

            # 重新保存MissionForm实例
            new_mission.save()
            mission_post_form.save()

            return redirect('myapp:mission_list')
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        mission_post_form = MissionForm()
        context = {'form': mission_post_form}
        return render(request, 'Mission/create.html', context)


@login_required
def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    mission = comment.mission
    if request.user == comment.user or request.user == mission.mission_taker:
        comment.delete()
    else:
        return HttpResponse('您无权删除此评论')
    return redirect('myapp:mission_detail', id=mission.id)



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

