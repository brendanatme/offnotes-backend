from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Folder(models.Model):
    user = models.ForeignKey(
        User,
        related_name="folders",
        on_delete=models.CASCADE,
        help_text="The user this folder belongs to",
        null=True,
    )
    name = models.CharField(max_length=100, help_text="Name of the folder")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the folder was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the folder was last updated"
    )

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(
        User,
        related_name="notes",
        on_delete=models.CASCADE,
        help_text="The user this note belongs to",
        null=True,
    )
    folder = models.ForeignKey(
        Folder,
        related_name="notes",
        on_delete=models.CASCADE,
        help_text="The folder this note belongs to",
    )

    title = models.CharField(max_length=200, help_text="Title of the note")
    date = models.DateField(
        help_text="Date associated with the note", blank=True, null=True
    )
    content = models.TextField(help_text="Full content/body of the note")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the note was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the note was last updated"
    )

    def __str__(self):
        return self.title
