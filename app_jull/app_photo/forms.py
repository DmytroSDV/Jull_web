from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, ImageField, TextInput, FileInput, FileField

from .models import Picture


def validate_file_size(value):
    # Максимальный размер файла в байтах (10 МБ)
    max_size = 10 * 1024 * 1024  # 10 МБ

    if value.size > max_size:
        raise ValidationError(f"Максимальный размер файла - 10 МБ. Ваш файл слишком большой ({value.size} байт).")



class FormPicture(ModelForm):
    description = CharField(max_length=200,widget=TextInput(attrs={'class':'form-control', 'id':'exampleInputEmail1'}))
    image = FileField(widget=FileInput(attrs={'class':'form-control', 'id':'formFile'}),validators=[validate_file_size])

    class Meta:
        model = Picture
        fields = ['description', 'image']
