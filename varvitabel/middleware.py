# your_app/middleware.py

from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = settings.LOGIN_URL or reverse('login')
        
        # Allow access to login/logout pages, admin, and static files
        allowed_paths = [
            login_url,
            reverse('logout') if    'logout' in settings.LOGIN_URL else '/logout/',
            reverse('register'),
            '/admin/',
            '/static/',
            '/media/',
        ]

        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in allowed_paths):
            return redirect(login_url)

        return self.get_response(request)
