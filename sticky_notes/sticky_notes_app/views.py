# sticky_notes_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import StickyNote

# Create your views here.
@login_required
def index(request):
    notes = StickyNote.objects.all()
    return render(request, 'sticky_notes_app/index.html', {'notes': notes})

@permission_required('sticky_notes_app.add_stickynote', login_url='index')
def add_note(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        content = request.POST.get('content')
        StickyNote.objects.create(author=author, title=title, content=content)
        # When done, return to the index.html page
        return redirect('index')
    return render(request, 'sticky_notes_app/add_note.html')

@login_required
def view_note(request, note_id):
    # Check if there is a valid entry
    note = get_object_or_404(StickyNote, id=note_id)
    return render(request, 'sticky_notes_app/view_note.html', {'note': note})

@permission_required('sticky_notes_app.change_stickynote', login_url='index')
# If the user does not have permission, they are redirected to homepage
def edit_note(request, note_id):
    # Check if there is a valid entry
    note = get_object_or_404(StickyNote, id=note_id)
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Update the StickyNote record
        note.author = author
        note.title = title
        note.content = content
        note.save()
        # Redirect to the view_note page
        return redirect('view_note', note_id=note.id)
    return render(request, 'sticky_notes_app/edit_note.html', {'note': note})

@permission_required('stick_notes_app.delete_stickynote', login_url='index')
# If the user does not have permission, they are redirected to homepage
def delete_note(request, note_id):
    # Check if there is a valid entry
    note = get_object_or_404(StickyNote, id=note_id)
    if request.method == 'POST':
        note.delete()
        # When done, return to the index.html page
        return redirect('index')
    return render(request, 'sticky_notes_app/delete_note.html', {'note': note})

