# sticky_notes_app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from .models import StickyNote

# Create your tests here.
class StickyNotesModelTest(TestCase):
    def setUp(self):
        # Create a sticky note for testing
        StickyNote.objects.create(title='Test Note', content='Test Content',
                                  author='Test Author')
        
    def test_note_has_title(self):
        # Test that a sticky note has the expected title
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.title, 'Test Note')

    def test_note_has_content(self):
        # Test that a sticky note has the expected content
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.content, 'Test Content')

    def test_note_has_author(self):
        # Test that a sticky note has the expected content
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.author, 'Test Author')


class StickyNotesViewTest(TestCase):
    def setUp(self):
        # Create the Posters group and add permissions
        posters_group, created = Group.objects.get_or_create(name='Posters')
        add_permission = Permission.objects.get(codename='add_stickynote')
        change_permission = Permission.objects.get(codename='change_stickynote')
        delete_permission = Permission.objects.get(codename='delete_stickynote')
        posters_group.permissions.add(add_permission, change_permission,
                                      delete_permission)
        # Create a test user and add them to the Posters group
        self.user = User.objects.create_user(username='testuser',
                                             password='testpw')
        self.user.groups.add(posters_group)
        self.client.login(username='testuser', password='testpw')
        # Create a sticky note for testing views
        StickyNote.objects.create(title='Test Note', content='Test Content',
                                  author='Test Author')

    def test_index_view(self):
        # Test the index view
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_view_note_view(self):
        # Test the view_note view
        note = StickyNote.objects.get(id=1)
        response = self.client.get(reverse('view_note', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'Test Content')

