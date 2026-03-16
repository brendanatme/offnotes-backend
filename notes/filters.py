import django_filters
from .models import Note


class NoteFilter(django_filters.FilterSet):
    folder = django_filters.NumberFilter(field_name="folder_id")

    class Meta:
        model = Note
        fields = ["folder"]
