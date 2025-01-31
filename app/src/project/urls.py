from django.conf import settings
from django.contrib.admin.sites import site
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .core.api import ChallengeViewSet, CompetitionViewSet, TaskSolutionViewSet
from .core.business_metrics import metrics_manager
from .core.metrics import metrics_view

api_router = DefaultRouter()
api_router.register("competitions", CompetitionViewSet)
api_router.register("challenges", ChallengeViewSet)
api_router.register("solutions", TaskSolutionViewSet)

urlpatterns = [
    path("admin/", site.urls),
    path("api/", include(api_router.urls)),
    path("api/auth/", include("rest_framework.urls")),
    path("metrics", metrics_view, name="prometheus-django-metrics"),
    path("business-metrics", metrics_manager.view, name="prometheus-business-metrics"),
    path("healthcheck/", include("health_check.urls")),
    path("", include("django.contrib.auth.urls")),
]

if settings.DEBUG_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
