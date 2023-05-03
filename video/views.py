from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import UploadImageForm, VideoTextForm
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import emoji 

from PIL import Image
import numpy as np 
import time 
import mimetypes
from wsgiref.util import FileWrapper
from django.conf import settings
from mutagen.mp3 import MP3 
from io import BytesIO
import os
from moviepy.editor import VideoFileClip
import string 
import random 
import datetime 
from pay.models import Subscription, Feature

import arabic_reshaper # pip install arabic-reshaper
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display # pip install python-bidi


os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Create your views here.

font_path = 'Cairo-Regular.ttf'

new_font = 'Lalezar-Regular.ttf'

new_font= 'Alexandria-VariableFont_wght.ttf' 


new_font = 'Changa-Regular.ttf'
new_font = 'NotoColorEmoji-Regular.ttf'

#new_font= 'NotoNaskhArabic-VariableFont_wght.ttf'



configuration = {
    "use_unshaped_instead_of_isolated": True
}

reshaper = ArabicReshaper(configuration=configuration)


@login_required
def combine_images(request):



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


    if features.template1 == True: 
        pass 
    else: 
        return redirect('/pay/plans/')



    if request.method == 'POST':


        
        if subscription.videos_per_months != 0: 



            # Get the uploaded images from the HTML form
            time_per_img = int(request.POST.get("time_per_img"))

            images = request.FILES.getlist('images')
            audio = request.FILES.get('audio') 

            audio_clip = AudioFileClip(audio.temporary_file_path()) 

            audio_file = afx.audio_loop(audio_clip, duration=((len(images) + 1)* time_per_img))

            res = request.POST.get('video-res') 

            end_text = request.POST.get('end_screen_text')
            end_url = request.POST.get('end_screen_url') 


            
            formated_end_text = []  
            for word in end_text.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_end_text.append(formated)

            end_text = get_display(' '.join(formated_end_text) )


            formated_end_url = []  
            for word in end_url.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_end_url.append(formated)

            end_url = get_display(' '.join(formated_end_url) )

            ### color clips here

            width = 0 
            height = 0
            font_size = 40

            if res=='facebook1':
                width = 1200
                height = 628 
            elif res=='facebook2':
                width = 810
                height = 450
            elif res == 'tiktok-snapchat':
                width = 1080
                height = 1920
                font_size = 60 
            elif res == 'square':
                width = 1080   
                height = 1080
                font_size = 60

            # Create a list of image paths
            image_paths = []
            for img in images:
                image_paths.append(img.temporary_file_path())

            # Create a video clip from the images using MoviePy
            # clips = [ImageClip(img_path).set_position("center", 'center').fx(vfx.resize, width=width).set_duration(time_per_img) for img_path in image_paths]
            
            clips =[] 

            # for img in image_paths:
            #     img = ImageClip(img).set_position('center', 'center').fx(vfx.resize, width=width).set_duration(time_per_img) 
            #     new_img = resize(img, height=height)
            #     new_img = new_img.fx(vfx.fadein, duration=.4)
            #     new_img = new_img.fx(transfx.slide_out, duration=.5, side='right')
            #     # new_img = new_img.resize(lambda t: 1 + 0.04 * t)  # Zoom-in effect
            #     clips.append(new_img)


            for img in image_paths:
                img = ImageClip(img).set_position('center', 'center').set_duration(time_per_img)
                if img.size[0] == img.size[1] and res=='tiktok-snapchat':
                    new_img = img.fx(vfx.resize, height=height)
                else:
                    new_img = img.fx(vfx.resize, height=height)
                    new_img = resize(img, width=width)
                # new_img = new_img.fx(vfx.fadeout, duration=.35)
                # new_img = new_img.fx(transfx.slide_out, duration=.5, side='left')
                new_img = new_img.resize(lambda t: 0.85 + 0.18 * t)  # Zoom-in effect
                clips.append(new_img)

            # top_text = arabic_reshaper.reshape(request.POST.get('top_text'))
            top_text = request.POST.get('top_text')
            formated_top_text = []  
            for word in top_text.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_top_text.append(formated)

            top_text = get_display(' '.join(formated_top_text) )
            top_text_with_emoji = emoji.emojize(top_text)
             
            
            # bottom_text = arabic_reshaper.reshape(request.POST.get('bottom_text')) 
            bottom_text = request.POST.get('bottom_text') 
            formated_bottom_text = []  
            for word in bottom_text.split(' '):
                formated = reshaper.reshape(word)
#                formated_bottom_text.append(arabic_reshaper.reshape(word)) 
                #text_to_display = get_display(formated)
                formated_bottom_text.append(formated) 
		
           # final_bottom_text = []
           # for word in formated_bottom_text:
           #     final_bottom_text.append(get_display(word)) 
            
 
            bottom_text = get_display(' '.join(formated_bottom_text ))
            bottom_text_with_emoji = emoji.emojize(bottom_text)



            top_text_clip = TextClip(txt=str(top_text_with_emoji), font=font_path ,fontsize=font_size, color='white').set_duration(time_per_img)
            bottom_text_clip = TextClip(txt=str(bottom_text_with_emoji), font=font_path ,fontsize=font_size ,color='white').set_duration(time_per_img)
            
            top_text_width, top_text_height = top_text_clip.size 
            bottom_text_width, bottom_text_height = bottom_text_clip.size 
            
            top_color_clip = ColorClip(size=(width, top_text_height+20), color=(0, 0, 0)).set_duration(time_per_img).set_position("top", "center")
            bottom_color_clip = ColorClip(size=(width, bottom_text_height+20), color=(0, 0, 0)).set_duration(time_per_img).set_position("center", "center")

            final_top_text_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip.set_position("center", "center")])
            final_bottom_text_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip.set_position("center", "center")])





            watermark = TextClip(txt='Video Editor', font=font_path, fontsize=30).set_opacity(.5).set_position(('center', 'center')).set_duration(time_per_img)

            ## this is final work list
            composite_clips = []

            

            if subscription.plan.price == 0: 
                for clip in clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center'), watermark], size=(width, height) )
                    # final_composite_clip = CompositeVideoClip([composite_clip, TextClip(txt='Video Editor', font=font_path, fontsize=30).set_position('center', 'center')])
                    composite_clips.append(composite_clip)
            
            else: 

                for clip in clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center')], size=(width, height))
                    composite_clips.append(composite_clip)


            end_screen = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(time_per_img).set_position("center", "center") 

            end_screen_text = TextClip(txt=end_text, color='white', font=font_path, fontsize=50).set_position(("center", "center")).set_duration(time_per_img) 
            end_screen_url = TextClip(txt=end_url, fontsize=30, color='black', font=font_path).set_duration(time_per_img)
            end_screen_url_color_clip = ColorClip(color=(255, 255, 255), size=(end_screen_url.size[0]+10, end_screen_url.size[1]+20)).set_duration(time_per_img)
            
            end_url_clip = CompositeVideoClip([end_screen_url_color_clip, end_screen_url.set_position(('center', "center"))]) 
            end_url_clip= end_url_clip.fx(transfx.slide_in, duration=1, side='left')

            end_clip = CompositeVideoClip([end_screen, end_screen_text, end_url_clip.set_position(("center", ((height / 2) + 40)))])

            composite_clips.append(end_clip) 

            video = concatenate_videoclips(composite_clips, method="chain").set_audio(audio_file)

            # Set the video file name and path
            video_file_name = 'my_video.mp4'
            video_file_path = 'media/' + video_file_name

            # Write the video file to disk
            # video.write_videofile(video_file_path, codec='libx264')
            video.write_videofile(video_file_path, fps=30)

            # Open the video file and create an HTTP response with the file contents
            with open(video_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename=' + video_file_name

            # Delete the video file from disk
            os.remove(video_file_path)

            subscription.videos_per_months -= 1 
            subscription.save() 

            return response 
        else: 
            subscription.delete() 
            return redirect('/pay/limit_ended/')

    else:
        return render(request, 'video/create_video.html')


@login_required
def remove_audio(request):


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


    if features.remove_audio == True: 
        pass 
    else:
        return redirect('/pay/plans/')


    if request.method == 'POST':

        video_file = request.FILES['video_file']

        # Save the uploaded video file to a temporary file
        with open('temp_video.mp4', 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        # Open the video file with MoviePy
        video_clip = VideoFileClip('temp_video.mp4')

        # Remove the audio from the video
        video_clip_without_audio = video_clip.without_audio()

        # Save the video to a new file
        new_filename = 'video_without_audio.mp4'
        video_clip_without_audio.write_videofile(new_filename)

        # Serve the video for download
        with open(new_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(new_filename))

        os.remove(new_filename)
        return response

    return render(request, 'video/remove_audio.html')


@login_required
def change_speed(request):


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

    if features.change_video_speed== True:
        pass 
    else: 
        return redirect('/pay/plans/')

    if request.method == 'POST':

        if subscription.videos_per_months != 0:

            video_file = request.FILES['video_file']
            speed_factor = float(request.POST['speed_factor'])

            # Save the uploaded video file to a temporary file
            with open('temp_video.mp4', 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Open the video file with MoviePy
            video_clip = VideoFileClip('temp_video.mp4')

            # Change the speed of the video
            new_video_clip = video_clip.fx(VideoFileClip.speedx, speed_factor)

            # Save the new video to a file
            new_filename = 'modified_video.mp4'
            new_video_clip.write_videofile(new_filename)

            # Serve the new video for download
            with open(new_filename, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(new_filename))

            os.remove(new_filename)

            subscription.videos_per_months -= 1
            subscription.save() 

            return response
        
        else:
            return redirect('/pay/plans/')

    return render(request, 'video/change_speed.html')



### إنشاء فيديو مع إضافة لوجو
@login_required
def combine_video_withlogo(request):

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
        return redirect('/pay/plans/') 



    features = Feature.objects.get(plan=subscription.plan)

    if features.template2 == True: 
        pass 
    else: 
        return redirect('/pay/plans/')

    if request.method == 'POST':

        if subscription.videos_per_months != 0: 


            # Get the input files from the HTML form
            images = request.FILES.getlist('image_files')
            audio = request.FILES['audio_file']
            logo = request.FILES['logo_file']
            tpi = request.POST['time_per_img']
            top_text = get_display(reshaper.reshape(request.POST['top_text']))
            bottom_text = get_display(reshaper.reshape(request.POST['bottom_text']) )

            end_text = request.POST.get('end_screen_text')
            end_url = request.POST.get('end_screen_url') 


            formated_end_text = []  
            for word in end_text.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_end_text.append(formated)

            end_text = get_display(' '.join(formated_end_text) )
             


            formated_end_url = []  
            for word in end_url.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_end_url.append(formated)

            end_url = get_display(' '.join(formated_end_url) )

            # Create a random filename for the output video
            filename = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.mp4')

            # Save the logo file to a temporary location
            with open('temp_logo.png', 'wb+') as destination:
                for chunk in logo.chunks():
                    destination.write(chunk)

            audio_clip = AudioFileClip(audio.temporary_file_path()) 

            audio_file = afx.audio_loop(AudioFileClip(audio.temporary_file_path()), duration=int((len(images) + 1) * int(tpi)))

            res = request.POST.get('video-res') 


            ### color clips here

            width = 0 
            height = 0
            font_size = 45

            if res=='facebook1':
                width = 1200
                height = 628 
            elif res=='facebook2':
                width = 810
                height = 450
            elif res == 'tiktok-snapchat':
                width = 1080
                height = 1920
                font_size = 65 
            elif res == 'square':
                width = 1080   
                height = 1080



            image_paths = []
            image_clips = []
            for img in images:
                image_paths.append(img.temporary_file_path())

            # Create a list of image clips
            # image_clips = [ImageClip(img_path, duration=int(tpi)) for img_path in image_paths]
            # image_clips = [ImageClip(img_path).set_position("center", 'center').fx(vfx.resize, height=height).set_duration(tpi) for img_path in image_paths]

            # for img_path in image_paths: 
            #     img = ImageClip(img_path) 
            #     # print(img.size) 
                
            #     # if img.size[0] < img.size[1]:
            #     new_img = img.set_position("center", 'center').fx(vfx.resize, width=width).set_duration(tpi)
            #     final_img = resize(new_img, height=height)
            #     # elif img.size[1] < img.size[0]:
            #     # new_img = new_img.fx(vfx.resize, height=height)
                
            #     image_clips.append(final_img)



            for img in image_paths:
                img = ImageClip(img).set_position('center', 'center').set_duration(tpi)
                if img.size[0] == img.size[1] and res=='tiktok-snapchat':
                    new_img = img.fx(vfx.resize, height=height)
                else:
                    new_img = img.fx(vfx.resize, height=height)
                    new_img = resize(img, width=width)
                # new_img = new_img.fx(vfx.fadeout, duration=.35)
                # new_img = new_img.fx(transfx.slide_out, duration=.5, side='left')
                new_img = new_img.resize(lambda t: 0.85 + 0.18 * t)  # Zoom-in effect
                image_clips.append(new_img)



            image_clips = []

            for img in image_paths:
                img = ImageClip(img).set_position('center', 'center').set_duration(tpi)
                if img.size[0] == img.size[1] and res=='tiktok-snapchat':
                    new_img = img.fx(vfx.resize, height=height)
                else:
                    new_img = img.fx(vfx.resize, height=height)
                    new_img = resize(img, width=width)
                new_img = new_img.fx(vfx.fadeout, duration=.35)
                new_img = new_img.resize(lambda t: 0.85 + 0.2 * t)  # Zoom-in effect
                image_clips.append(new_img)


            top_text_clip = TextClip(txt=str(top_text), font=font_path ,fontsize=font_size, color='white').set_duration(tpi)
            bottom_text_clip = TextClip(txt=str(bottom_text), font=font_path ,fontsize=font_size ,color='white').set_duration(tpi)
            
            top_text_width, top_text_height = top_text_clip.size 
            bottom_text_width, bottom_text_height = bottom_text_clip.size 
            
            top_color_clip = ColorClip(size=(width, top_text_height+20), color=(0, 0, 0)).set_duration(tpi).set_position("top", "center")
            bottom_color_clip = ColorClip(size=(width, bottom_text_height+20), color=(0, 0, 0)).set_duration(tpi).set_position("center", "center")

            final_top_text_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip.set_position("center", "center")])
            final_bottom_text_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip.set_position("center", "center")])

            ## this is final clips list
            composite_clips = []

            watermark = TextClip(txt='Video Editor', font=font_path, fontsize=30).set_opacity(.5).set_position(('center', 'center')).set_duration(tpi)


#            if subscription.plan.price ==0: 
                ## here, the video will produced with watermark
#                for clip in image_clips:
#                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center'), watermark], size=(width, height))
#                    composite_clips.append(composite_clip)
#            else: 
                # without watermark
#                for clip in image_clips:
#                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center')], size=(width, height))
#                    composite_clips.append(composite_clip)

            # Concatenate the image clips into a video clip
#            video_clip = concatenate_videoclips(composite_clips, method='compose').set_audio(audio_file)


            # Load the logo image using moviepy
            #logo_clip = ImageClip('temp_logo.png', transparent=True).set_duration(video_clip.duration).resize(height=top_text_height) 


            # END SCREEN SETTINGS



            end_screen = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(tpi).set_position("center", "center") 

            end_screen_text = TextClip(txt=end_text, color='white', font=font_path, fontsize=50).set_position(("center", "center")).set_duration(tpi) 
            end_screen_url = TextClip(txt=end_url, fontsize=30, color='black', font=font_path).set_duration(tpi)
            end_screen_url_color_clip = ColorClip(color=(255, 255, 255), size=(end_screen_url.size[0]+10, end_screen_url.size[1]+20)).set_duration(tpi)
            
            end_url_clip = CompositeVideoClip([end_screen_url_color_clip, end_screen_url.set_position(('center', "center"))]) 
            end_url_clip= end_url_clip.fx(transfx.slide_in, duration=1, side='left')

            end_clip = CompositeVideoClip([end_screen, end_screen_text, end_url_clip.set_position(("center", ((height / 2) + 40)))])

            # composite_clips.append(end_clip) 


            if subscription.plan.price ==0: 
                ## here, the video will produced with watermark
                for clip in image_clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center'), watermark], size=(width, height))
                    composite_clips.append(composite_clip)
            else: 
                # without watermark
                for clip in image_clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center')], size=(width, height))
                    composite_clips.append(composite_clip)

            # Concatenate the image clips into a video clip
            video_clip = concatenate_videoclips(composite_clips, method='chain').set_audio(audio_file)


            # Load the logo image using moviepy
            logo_clip = ImageClip('temp_logo.png', transparent=True).set_duration(video_clip.duration).resize(height=top_text_height+10) 

            # Add the logo to the video clip
            video_clip = CompositeVideoClip([video_clip, logo_clip.set_position((7.5, 10))])

            # final = concatenate_videoclips([video_clip], method='chain')
            

            # Save the final video to the output file
            video_clip.write_videofile(filename, fps=25, threads=12, preset='veryfast', codec='libx264')

            # Serve the video file for download
            with open(filename, 'rb') as video:
                response = HttpResponse(video.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename=output_video.mp4'

            # Delete the temporary files
            os.remove(filename)
            os.remove('temp_logo.png')



            subscription.videos_per_months -= 1 
            subscription.save() 

            return response
        else: 
            return redirect('/pay/plans/')

    return render(request, 'video/combine_video_withlogo.html')





# هنا نموذج الفيديو الثالث

@login_required
def feedback_video_template(request):


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



    if features.template3 == True: 
        pass 
    else: 
        return redirect('/pay/plans/')


    if request.method == 'POST': 


        if subscription.videos_per_months != 0: 


            video = request.FILES['video']
            background = request.FILES['background']
            text = request.POST['text']
            text = get_display(reshaper.reshape(text)) 
            res = request.POST.get('video-res') 
            fontsize = request.POST.get('fontsize')

            video = VideoFileClip(video.temporary_file_path()).set_position(('center', 'center'))
            duration = video.duration 


            width = 0 
            height = 0

            if res=='facebook1':
                width = 1200
                height = 628 
            elif res=='facebook2':
                width = 810
                height = 450
            elif res == 'tiktok-snapchat':
                width = 1080
                height = 1920


            maskclip=ImageClip("mask1.png",ismask=True).set_duration(duration) 
            resized_mask = resize(maskclip, width=((width/2) - 50))
            m_width, m_height = resized_mask.size 


            text_clip_size = (width - m_width - 100, 0) 

            ## Text Clip Here 
            text_clip = TextClip(txt=text, color='gold', size=text_clip_size, font=font_path).set_duration(video.duration).set_position('right', 'center')

            ## Text Clip Size : (width - mask_width) - 50 , height = 0  


            img = ImageClip(background.temporary_file_path(), duration=duration)
            img = img.fx(vfx.resize, width=width)

            # Resized Image
            resized = resize(img.set_position(('center', 'center')), height=height) 
            r_width, r_height = resized.size 


            # Resized Video 
            resized_video = resize(video, width=m_width) 

            # resized_video = resized_video.set_mask(resized_mask)

            # top_text_clip = TextClip(txt="Ramadan Kareem", fontsize=20, color='white', size=((0, 0))).set_duration(duration).set_position('center', 'center')
            # bottom_text_clip = TextClip(txt="Amazing Sales in Ramadan", fontsize=20, color='white', size=((0, 0))).set_duration(duration).set_position('center', 'center')

            # t_text_width, t_text_height = top_text_clip.size 


            # top_color_clip = ColorClip(size=(r_width, t_text_height+20), color=(0, 0, 0)).set_duration(duration).set_position("top", "center")
            # bottom_color_clip = ColorClip(size=(r_width, t_text_height+20), color=(0, 0, 0)).set_duration(duration).set_position("center", "center")


            # top_text_work_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip])
            # bottom_text_work_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip])

            # part1 = CompositeVideoClip(clips=[resized, top_text_work_clip])

            # part2 = CompositeVideoClip([part1, bottom_text_work_clip.set_position("bottom", "center")])



            watermark = TextClip(txt='Video Editor', font=font_path, fontsize=30).set_opacity(.5).set_position(('center', 'center')).set_duration(duration)

            final = CompositeVideoClip([resized, resized_video.set_position((50, 'center'))], size=(width, height))

            
            if subscription.plan.price ==0: 
                ### الفيديو مع علامة مائية
                final2 = CompositeVideoClip([final, text_clip.set_position((width-text_clip_size[0] -20, 'center')), watermark], size=(width, height)) 
            else: 
                final2 = CompositeVideoClip([final, text_clip.set_position((width-text_clip_size[0] -20, 'center'))], size=(width, height)) 

        
            # top_text_work_clip.save_frame('out.png')

            final2.write_videofile("out.mp4", fps=25, threads=10, preset='veryfast', codec='libx264')

            ## DOWNLOAD FILE
            with open('out.mp4', 'rb') as video:
                response = HttpResponse(video.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename=output_video.mp4'

            # Delete the temporary files
            os.remove('out.mp4')

            subscription.videos_per_months -=1 
            subscription.save() 

            return response
        else: 
            return redirect('/pay/plans/')

    return render(request, 'video/create_feedback_video.html', {})
