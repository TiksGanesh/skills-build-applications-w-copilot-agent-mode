"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')

# Build API root URLs using $CODESPACE_NAME to avoid HTTPS certificate issues
_CODESPACE_NAME = os.environ.get('CODESPACE_NAME')
_BASE_URL = (
    f"https://{_CODESPACE_NAME}-8000.app.github.dev" if _CODESPACE_NAME else "http://localhost:8000"
)

def api_root(_request):
    return JsonResponse({
        'users': f"{_BASE_URL}/api/users/",
        'teams': f"{_BASE_URL}/api/teams/",
        'activities': f"{_BASE_URL}/api/activities/",
        'workouts': f"{_BASE_URL}/api/workouts/",
        'leaderboards': f"{_BASE_URL}/api/leaderboards/",
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root'),
]
