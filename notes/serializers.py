from rest_framework import serializers
from .models import Folder, Note


class FolderSerializer(serializers.ModelSerializer):
    """
    Serializer for Folder model.
    
    Fields:
    - id: Unique identifier (read-only)
    - name: Folder name
    - notes_count: Number of notes in the folder (read-only)
    - created_at: Creation timestamp (read-only)
    - updated_at: Last update timestamp (read-only)
    """
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ["id", "name", "notes_count", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_notes_count(self, obj):
        """Return the number of notes in the folder."""
        return obj.notes.count()


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model.
    
    Fields:
    - id: Unique identifier (read-only)
    - folder: Foreign key to the parent folder
    - title: Note title
    - date: Date of the note
    - content: Full content of the note
    - created_at: Creation timestamp (read-only)
    - updated_at: Last update timestamp (read-only)
    """
    class Meta:
        model = Note
        fields = [
            "id",
            "folder",
            "title",
            "date",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
