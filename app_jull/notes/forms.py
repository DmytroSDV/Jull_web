from django.forms import ModelForm, CharField, ImageField, TextInput, FileInput, FileField

from .models import Note


class NoteForm(ModelForm):
    content = CharField(max_length=1000,widget=TextInput(attrs={'class':'form-control', 'id':'exampleInputEmail1'}))
    tags = CharField(max_length=1000,widget=TextInput(attrs={'class':'form-control', 'id':'exampleInputEmail1'}))

    class Meta:
        model = Note
        fields = ['content', 'tags']


class SearchNoteForm(ModelForm):
    tags = CharField(max_length=1000, widget=TextInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))

    class Meta:
        model = Note
        fields = ['tags']