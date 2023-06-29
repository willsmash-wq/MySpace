from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 定义在验证码未验证时，用户可以访问的页面
        unvalidated_pages = [reverse('shou'), reverse('refresh_captcha'), reverse('test')]
        # 定义在验证码已验证但用户未登录时，用户可以访问的页面
        captcha_validated_pages = [reverse('userprofile:login'), reverse('userprofile:register'),
                                   reverse('userprofile:registered_users'), reverse('userprofile:check-username')]

        # 如果用户未通过验证码验证
        if not request.session.get('captcha_validated', False):
            # 只允许用户访问 unvalidated_pages 定义的页面
            if not request.path_info.startswith('/captcha/') and request.path_info not in unvalidated_pages:
                return redirect('shou')  # 如果用户试图访问其他页面，则重定向到验证码页面
        # 如果用户已经通过了验证码验证，但是还没有登录
        elif not request.user.is_authenticated:
            # 只允许用户访问 captcha_validated_pages 定义的页面
            if request.path_info not in captcha_validated_pages:
                return redirect('userprofile:login')  # 如果用户试图访问其他页面，则重定向到登录页面
        # 如果用户已经登录，则不做任何限制，允许访问所有页面

        response = self.get_response(request)
        return response
