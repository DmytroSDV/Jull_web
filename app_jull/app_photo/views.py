import cloudinary.uploader
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormPicture
from .models import Picture
from os.path import splitext


# Create your views here.


# def upload(request):
#     form = FormPicture(instance=Picture())
#     if request.method == 'POST':
#         form = FormPicture(request.POST, request.FILES, instance=Picture())
#         if form.is_valid():
#             form.save()
#             return render(request, 'app_photo/upload.html', context={'form': form})
#     return render(request, 'app_photo/upload.html', context={'form': form})



def get_file_type(url):
    _, ext = splitext(url)
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'image'
    elif ext.lower() in ['.txt']:
        return 'text'
    elif ext.lower() in ['.mp4', '.avi', '.mov']:
        return 'video'
    else:
        return 'unknown'

def show_images(request):
    images = Picture.objects.all()

    image_data = [
        {
            'url': image.image.url,
            'description': image.description,
            'id': image.id,
            'file_type': get_file_type(image.image.url)
        } for image in images
    ]


    return render(request, 'app_photo/image_gallery.html', {'image_data': image_data})



def upload(request):
    if request.method == 'POST':
        form = FormPicture(request.POST, request.FILES)
        if form.is_valid():
            # Получаем файл из формы
            file = request.FILES.get('image')
            if file:
                # Загружаем файл на Cloudinary
                uploaded_file = cloudinary.uploader.upload(file, resource_type="raw")  # Указываем тип файла как "raw"

                # Сохраняем описание и URL загруженного файла в модели Picture
                picture = form.save(commit=False)
                picture.description = form.cleaned_data['description']
                picture.image = uploaded_file['secure_url']  # URL загруженного файла
                picture.save()

                return render(request, 'app_photo/upload.html', {'form': form})
    else:
        form = FormPicture()
    return render(request, 'app_photo/upload.html', {'form': form})



def delete_image(request, image_id):
    try:
        image = Picture.objects.get(id=image_id)
        image.image.delete()
        image.delete()
        return redirect(to='app_photo:gallery')
    except Picture.DoesNotExist:
        return redirect(to='app_photo:gallery')


def edit_image(request,image_id):
    if request.method == 'POST':
        desc=request.POST.get('description')
        Picture.objects.filter(id=image_id).update(description=desc)

        return redirect(to='app_photo:gallery')
    data=Picture.objects.filter(id=image_id).first()

    return render(request,'app_photo/edit_form.html',context={'data':data})



def download_image(request, image_id):
    try:
        # Получаем объект Picture по его идентификатору
        picture = Picture.objects.get(id=image_id)
        # Получаем URL изображения из поля image объекта Picture
        image_url = picture.image.url
        # Получаем содержимое изображения по его URL с помощью запроса
        response = requests.get(image_url)
        # Получаем расширение файла изображения из его URL
        type_file=picture.image.url.split('.').pop()
        # Создаем HTTP-ответ с содержимым изображения
        http_response = HttpResponse(response.content, content_type='image/jpeg')
        # Устанавливаем заголовок для скачивания
        http_response['Content-Disposition'] = f'attachment; filename={picture.description}.{type_file}'
        return http_response
    except Exception as e:
        # Обработка ошибок, если изображение не найдено или произошла другая ошибка
        return HttpResponse("Error: " + str(e))

def show_all_photo(request):
    images = Picture.objects.all()

    image_data = [
        {
            'url': image.image.url,
            'description': image.description,
            'id': image.id,
            'file_type': get_file_type(image.image.url)
        } for image in images
    ]


    return render(request, 'app_photo/photos.html', {'image_data': image_data})


def show_all_video(request):
    images = Picture.objects.all()

    image_data = [
        {
            'url': image.image.url,
            'description': image.description,
            'id': image.id,
            'file_type': get_file_type(image.image.url)
        } for image in images
    ]


    return render(request, 'app_photo/videos.html', {'image_data': image_data})

def show_all_another(request):
    images = Picture.objects.all()

    image_data = [
        {
            'url': image.image.url,
            'description': image.description,
            'id': image.id,
            'file_type': get_file_type(image.image.url)
        } for image in images
    ]


    return render(request, 'app_photo/another_files.html', {'image_data': image_data})