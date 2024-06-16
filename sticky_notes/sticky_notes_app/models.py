# sticky_notes_app/models.py

from django.db import models

# Create your models here.

class StickyNote(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=30)
    # Create a display to make the data easier to read in admin panel
    def __str__(self):
        return self.title