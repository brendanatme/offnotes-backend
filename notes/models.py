from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the folder")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the folder was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the folder was last updated")

    def __str__(self):
        return self.name


class Note(models.Model):
    folder = models.ForeignKey(Folder, related_name="notes", on_delete=models.CASCADE, help_text="The folder this note belongs to")

    title = models.CharField(max_length=200, help_text="Title of the note")
    date = models.DateField(help_text="Date associated with the note", auto_now_add=True)
    content = models.TextField(help_text="Full content/body of the note")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the note was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the note was last updated")

    def __str__(self):
        return self.title
