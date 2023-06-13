from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 列出所有允许未登录用户访问的URL
        unauthenticated_pages = [reverse('userprofile:login'), reverse('userprofile:register')]
        if not request.user.is_authenticated:
            # 如果请求的URL不在允许访问的列表中，就重定向到登录页面
            if request.path not in unauthenticated_pages:
                return redirect('userprofile:login')
        response = self.get_response(request)
        return response
