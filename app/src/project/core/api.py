from rest_framework.viewsets import ModelViewSet

from .models import Competition
from .serializers import CompetitionSerializer


class CompetitionViewSet(ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = tuple()
