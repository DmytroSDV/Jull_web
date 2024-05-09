from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .forms import NoteForm,SearchNoteForm
from .models import Note, Tag
from django.contrib import messages

# Create your views here.


def show_notes(request,page=1):
    user=request.user
    notes = Note.objects.filter(user=user)
    paginator = Paginator(notes, 5)
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    return render(request, "notes/mynotes.html", context={"notes": notes})


def delete_note(request, notes_id):
    try:
        note = Note.objects.get(id=notes_id)
        note.delete()
        return redirect(to='notes:notes_list')
    except Note.DoesNotExist:
        return redirect(to='notes:notes_list')


def edit_note(request, notes_id):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            tags_input = form.cleaned_data['tags']
            # Розділіть введені теги на окремі теги
            tags_list = [tag.strip() for tag in tags_input.split()]
            # Отримайте запис для редагування
            note = Note.objects.get(id=notes_id)
            note.content = content
            note.save()  # Зберегти зміни у записі
            # Очистити старі теги
            note.tags.clear()
            # Додати нові теги
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(tag=tag_name)
                note.tags.add(tag)
            return redirect('notes:notes_list')
    else:
        note = Note.objects.get(id=notes_id)
        # Створити форму з даними про запис
        form = NoteForm(initial={'content': note.content, 'tags': ' '.join(note.tags.values_list('tag', flat=True))})
    return render(request, 'notes/edit_note.html', {'form': form})


def add_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            tag_data = form.cleaned_data['tags']
            tag_names = tag_data.split()  # Перетворити рядок тегів на список
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(tag=tag_name.strip())
                note.tags.add(tag)  # Додати тег до запису
            messages.success(request, 'Заметка успешно создана.')
            return redirect('notes:notes_list')
        else:
            # Если форма не прошла валидацию, добавляем сообщение об ошибке
            messages.error(request, 'Заметка не создана. Пожалуйста, заполните все поля формы.')
    else:
        form = NoteForm()
    return render(request, 'notes/add_notes.html', {'form': form})


def search_notes(request):
    if request.method == 'POST':
        form = SearchNoteForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            # Виконати логіку пошуку за тегами та отримати результати
            notes = Note.objects.filter(tags__tag__icontains=tags)
            return render(request, 'notes/search_results.html', {'notes': notes, 'form': form})
    else:
        form = SearchNoteForm()
    return render(request, 'notes/search_notes.html', {'form': form})


def notes_by_tag(request, tag):
    user = request.user
    notes = Note.objects.filter(tags__tag__iexact=tag, user=user)
    if not notes.exists():
        messages.info(request, f'Заметок с тегом "{tag}" не найдено.')
    return render(request, 'notes/notes_by_tag.html', {'notes': notes, 'tag': tag})
