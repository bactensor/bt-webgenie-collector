import json
from io import StringIO
from urllib.parse import urlparse

from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from .models import Challenge, Competition, TaskSolution
from .serializers import ChallengeDetailsSerializer, CompetitionSerializer, TaskSolutionSerializer


class CompetitionViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class HasValidReferralPermission(BasePermission):
    message = "Invalid referrer"

    def has_permission(self, request: Request, view) -> bool:
        referrer = request.headers.get("referer", "")
        return urlparse(referrer).hostname in settings.REST_FRAMEWORK_ALLOWED_REFERRERS

class DownloadOnlyIfReferralMixin(GenericViewSet):
    def get_permissions(self, *args, **kwargs) -> list[BasePermission]:
        if self.action == "download":
            self.permission_classes += (HasValidReferralPermission,)
        return super().get_permissions(*args, **kwargs)


class ChallengeViewSet(DownloadOnlyIfReferralMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeDetailsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True)
    def download(self, request: Request, *args, **kwargs) -> StreamingHttpResponse:
        challenge = self.get_object()
        return StreamingHttpResponse(
            StringIO(challenge.ground_truth_html),
            content_type="text/plain; charset=UTF-8",
            headers={
                "Content-Disposition": f'attachment; filename="challenge{challenge.id}.html"',
            },
        )


class TaskSolutionViewSet(DownloadOnlyIfReferralMixin, RetrieveModelMixin, GenericViewSet):
    queryset = TaskSolution.objects.all()
    serializer_class = TaskSolutionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True)
    def download(self, request: Request, *args, **kwargs) -> StreamingHttpResponse:
        solution = self.get_object()
        return StreamingHttpResponse(
            StringIO(json.dumps(solution.miner_answer)),
            content_type="application/json; charset=UTF-8",
            headers={
                "Content-Disposition": f'attachment; filename="solution{solution.id}.json"',
            },
        )
