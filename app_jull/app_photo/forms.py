from django.forms import ModelForm, CharField, ImageField, TextInput, FileInput, FileField

from .models import Picture


class FormPicture(ModelForm):
    description = CharField(max_length=200,widget=TextInput(attrs={'class':'form-control', 'id':'exampleInputEmail1'}))
    image = FileField(widget=FileInput(attrs={'class':'form-control', 'id':'formFile'}))

    class Meta:
        model = Picture
        fields = ['description', 'image']
