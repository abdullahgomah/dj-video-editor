from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image 
import numpy as np 
import os 

# Create your views here.

def changesize(request):
    if request.POST:
        img = request.FILES.get('image')
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))

        img_file = Image.open(img) 
        img_file.load()
        img_file_name = 'resized_img.png'
        img_file_path = 'media/' + img_file_name
        img_file = img_file.resize(size=(width, height)).save(img_file_path)

        with open(img_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/x-png')
            response['Content-Disposition'] = 'attachment; filename=' + img_file_name

        # Delete the video file from disk
        os.remove(img_file_path)

        return response

    else:
        return render(request, 'image/changesize.html')

