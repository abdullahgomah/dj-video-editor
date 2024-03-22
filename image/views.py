from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from pay.models import Subscription, Feature
import datetime 
from PIL import Image 
import numpy as np 
import os 
import zipfile 
from django.contrib import messages 
from moviepy.editor import *
from io import StringIO
import uuid 

# Create your views here.






@login_required
def changesize(request):


    user = request.user 


    try:
        subscription = Subscription.objects.get(user=user)
        if subscription: 
            if datetime.date.today() > subscription.end_date_time: 
                # print('Please Renew Your Subscription')
                # هنا يجب تجديد الاشتراك
                subscription.delete()
                return redirect('/pay/plans/') 
    except:
        return redirect('/pay/plans') 

    
    features = Feature.objects.get(plan=subscription.plan)

    if features.change_img_size == True:
        pass 
    else: 
        return redirect('/pay/plans/')



    if request.POST:

        img = request.FILES.get('image')

        print(img)
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))

        img_file = Image.open(img) 
        img_file.load()
        img_file_name = 'resized_img.png'
        # دي اتعدلت في السيرفر بس ما اتعدلتش هنا
        img_file_path = img_file_name
        img_file = img_file.resize(size=(width, height)).save(img_file_path)

        with open(img_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/x-png')
            response['Content-Disposition'] = 'attachment; filename=' + img_file_name

        # Delete the video file from disk
        os.remove(img_file_path)

        return response

    else:
        return render(request, 'image/changesize.html')


def bulk_size_change(request): 
    if request.POST: 
        images = request.FILES.getlist('images-input') 
        size = request.POST.get('size-input') 
        width = 0 
        height = 0 

        if size is not None and size is not "": 
            if size == 'instagram-story': 
                width = 1080 
                height = 1920 
            elif size == 'facebook-landscape': 
                width = 1280 
                height = 720 
            elif size == 'facebook-portrait': 
                width = 720 
                height = 1280 
            elif size == 'square': 
                width = 1080 
                height = 1080 
            else: 
                ## send error message 
                messages.add_message(request, messages.ERROR, message='يرجي اختيار حجم مناسب')
                return redirect("image:bulk-change-size")

        clips = []
        for img in images: 
            img_path = img.temporary_file_path() 
            clip = ImageClip(img_path).set_position('center', 'center')
            if clip.size[0] > clip.size[1]: 
                clip = clip.resize(height=height)  
            elif clip.size[0] == clip.size[1]: 
                ## square case 
                if height > width: 
                    clip = clip.resize(width=width) 
                else: 
                    clip = clip.resize(height=height)  
                
            else: 
                clip = clip.resize(width=width)
            
            clip = clip.set_position('center','center').set_duration(1) 
            final_clip = CompositeVideoClip([clip], size=((width, height)))

            clips.append(final_clip)
        
        print(clips) 

        file_list = [] 
        for clip in clips: 
            filename = uuid.uuid4().hex[:10].upper()
            file_path = './' + filename +'.png'
            # clip.write_videofile(file_path, fps=1, codec='image/png') 
            clip.write_videofile(file_path, fps=1, codec='png') 

            file_list.append(file_path) 
        

        s = StringIO() 
        zip_file_name= f'{uuid.uuid4().hex[:12]}.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip:

            for f in file_list: 
                zip.write(f) 
        
        print('Zipped Successfully')

        with open(zip_file_name, 'rb') as file: 
            resp = HttpResponse(file.read(), content_type='application/x-zip-compressed')
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_file_name

            return resp 
        


        return redirect("image:bulk-change-size")

    context = {} 
    return render(request, 'image/bulk-size-change.html', context)