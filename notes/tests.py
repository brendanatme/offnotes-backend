from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Folder, Note

User = get_user_model()


class NotesApiTest(APITestCase):
    def setUp(self):
        # two users with separate objects
        self.user1 = User.objects.create_user(username="alice", password="pass")
        self.user2 = User.objects.create_user(username="bob", password="pass")

        # Folders for each
        self.folder1 = Folder.objects.create(user=self.user1, name="Alice's Folder")
        self.folder2 = Folder.objects.create(user=self.user2, name="Bob's Folder")

        # Notes for each
        self.note1 = Note.objects.create(
            user=self.user1,
            folder=self.folder1,
            title="Alice note",
            content="hello",
        )
        self.note2 = Note.objects.create(
            user=self.user2,
            folder=self.folder2,
            title="Bob note",
            content="hi",
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_folders_filtered_by_user(self):
        self.authenticate(self.user1)
        url = reverse('folder-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # should only see user1 folder
        names = [f['name'] for f in resp.data]
        self.assertIn(self.folder1.name, names)
        self.assertNotIn(self.folder2.name, names)

    def test_notes_filtered_by_user(self):
        self.authenticate(self.user1)
        url = reverse('note-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [n['title'] for n in resp.data]
        self.assertIn(self.note1.title, titles)
        self.assertNotIn(self.note2.title, titles)

    def test_note_creation_sets_user_and_validates_folder(self):
        self.authenticate(self.user1)
        url = reverse('note-list')
        data = {'folder': self.folder1.id, 'title': 'new', 'content': 'hi'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(id=resp.data['id'])
        self.assertEqual(note.user, self.user1)

        # cannot create note in someone else's folder
        data['folder'] = self.folder2.id
        resp2 = self.client.post(url, data)
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
