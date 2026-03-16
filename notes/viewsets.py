from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Folder, Note
from .serializers import FolderSerializer, NoteSerializer
from .filters import NoteFilter


from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=['Folders'],
    operation_id='folders_create',
)
class FolderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing folders.
    
    Provides CRUD operations for folders:
    - list: Get all folders (owned by the requesting user)
    - create: Create a new folder, automatically assigned to the user
    - retrieve: Get a specific folder with its details
    - update: Update a folder
    - partial_update: Partially update a folder
    - destroy: Delete a folder
    
    Requires authentication with a valid token.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FolderSerializer

    def get_queryset(self):
        # always limit to folders owned by the authenticated user
        user = self.request.user
        return Folder.objects.filter(user=user)

    def perform_create(self, serializer):
        # assign the current user when creating
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # save the updated instance
        serializer.save()


@extend_schema(
    tags=['Notes'],
    operation_id='notes_create',
)
class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notes.
    
    Provides CRUD operations for notes:
    - list: Get all notes (owned by the requesting user, newest first)
    - create: Create a new note, assigned to the user
    - retrieve: Get a specific note with its details
    - update: Update a note
    - partial_update: Partially update a note
    - destroy: Delete a note
    
    Supports filtering by folder via query parameter.
    Requires authentication with a valid token.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteFilter

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
