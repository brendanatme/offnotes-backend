from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Folder, Note
from .serializers import FolderSerializer, NoteSerializer
from .filters import NoteFilter


@extend_schema(tags=['Folders'])
class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FolderSerializer
    queryset = Folder.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Folder.objects.none()
        return Folder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Notes'])
class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteFilter
    queryset = Note.objects.none()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Note.objects.none()
        return Note.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
