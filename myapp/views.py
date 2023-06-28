
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
import calendar
from datetime import datetime
from userprofile.forms import DepartmentTeamForm
from .forms import MissionForm, CommentForm, ArticleTypeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Mission, Comment, MissionRating
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
@login_required
def mission_detail(request, id):
    mission = get_object_or_404(Mission, id=id)
    new_comment = None
    user_rating = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.mission = mission
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    if request.user.is_authenticated:
        user_rating = MissionRating.objects.filter(mission=mission, user=request.user).first()

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

    context = {
        'mission': mission,
        'toc': md.toc,
        'comments': mission.comments.all(),
        'new_comment': new_comment,
        'comment_form': comment_form,
        'user_rating': user_rating,
    }

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
    if request.method == "POST":
        mission_form = MissionForm(request.POST, instance=mission)
        if mission_form.is_valid():
            mission_form.save()
            return redirect("myapp:mission_detail", id=id)
        else:
            return HttpResponse("表单内容有误,请重新填写")
    else:
        mission_form = MissionForm(instance=mission)
        context = {'mission': mission, 'form': mission_form}
        return render(request, 'Mission/update.html', context)


from django.http import JsonResponse
import json


@login_required
def mission_rating(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating', 0)
        mission = get_object_or_404(Mission, id=id)
        user = request.user

        mission_rating, created = MissionRating.objects.get_or_create(mission=mission, user=user)
        if created:
            mission_rating.rating = rating
            mission_rating.save()
            return JsonResponse({'message': '评分保存成功'})
        else:
            return JsonResponse({'message': '你已经评过分了，不能再评分'}, status=400)

    else:
        return JsonResponse({'message': '无效的请求方法'}, status=400)


from django.db.models import Count, Sum, F


def contribution_rank_view(request):
    users = User.objects.annotate(
        total_missions=Count('taken_missions', distinct=True),
        total_views=Sum('taken_missions__total_views', distinct=True),
        total_comments=Count('taken_missions__comments', distinct=True),
        total_rating=Sum('taken_missions__missionrating__rating', distinct=True),
    ).order_by('-total_views')

    weighted_scores = []
    for user in users:
        missions = user.taken_missions.all()
        weighted_score = sum(
            mission.total_views * (mission.missionrating_set.aggregate(average=Avg('rating'))['average'] or 0) for
            mission in missions)
        weighted_scores.append(weighted_score)

    medals = ['🥇', '🥈', '🥉'] + [''] * (len(users) - 3)  # create a list of medals

    context = {
        'users': zip(users, weighted_scores, medals)
    }

    return render(request, 'Mission/contribution_rank.html', context)


def team_contribution(request):
    # 获取当前月份的起始日期和结束日期
    year = datetime.now().year
    month = datetime.now().month
    start_date, end_date = calendar.monthrange(year, month)
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, end_date)
    form = ArticleTypeForm(request.GET)

    # 如果表单有效（用户选择了一个文章类型）
    if form.is_valid():
        selected_type = form.cleaned_data.get('article_type')
    else:
        selected_type = Mission.ARTICLE_TYPE_CHOICES[0][0]

    # 获取每个班组的发布数量并排序
    teams = DepartmentTeamForm.TEAM_CHOICES
    team_counts = []
    for team_choice in teams:
        team = team_choice[0]
        count = Mission.objects.filter(mission_taker__profile__team=team, article_type=selected_type,
                                       created__range=(start_date, end_date)).count()
        team_counts.append((team, count))

    # 根据发布数量降序排序
    team_counts.sort(key=lambda x: x[1], reverse=True)

    context = {
        'form': form,
        'team_counts': team_counts
    }
    return render(request, 'Mission/team_contribution.html', context)