from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from pay.models import Subscription, Feature
import datetime 
from PIL import Image 
import numpy as np 
import os 

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

