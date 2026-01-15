from rest_framework import viewsets
from .models import Folder, Note
from .serializers import FolderSerializer, NoteSerializer


class FolderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing folders.
    
    Provides CRUD operations for folders:
    - list: Get all folders
    - create: Create a new folder
    - retrieve: Get a specific folder with its details
    - update: Update a folder
    - partial_update: Partially update a folder
    - destroy: Delete a folder
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notes.
    
    Provides CRUD operations for notes:
    - list: Get all notes (ordered by date, newest first)
    - create: Create a new note
    - retrieve: Get a specific note with its details
    - update: Update a note
    - partial_update: Partially update a note
    - destroy: Delete a note
    """
    queryset = Note.objects.all().order_by('-date')
    serializer_class = NoteSerializer
