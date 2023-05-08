
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import redirect, render 
from moviepy.editor import *
from moviepy.video.fx.resize import resize

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


configuration = {
    "use_unshaped_instead_of_isolated": True
}

reshaper = ArabicReshaper(configuration=configuration)



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


    if features.video_imgs_template == True: 
        pass 
    else: 
        return redirect('/pay/plans/')



    if request.method == 'POST':


        
        if subscription.videos_per_months != 0: 



            # Get the uploaded images from the HTML form
            time_per_img = int(request.POST.get("time_per_img"))

            final_duration = 0 

            images = request.FILES.getlist('images')
            




            # audio_file = afx.audio_loop(audio_clip, duration=((len(images) + 1)* time_per_img))

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
            clips =[] 




            for img in images:
                img_path = img.temporary_file_path()
                img_path_content_type = img.content_type

                print(img_path_content_type) 

                if str(img_path_content_type).startswith('image/'): 
                    img = ImageClip(img_path).set_position('center', 'center').set_duration(time_per_img)
                    img = img.set_duration(time_per_img)
                elif str(img_path_content_type).startswith('video/'): 
                    img = VideoFileClip(img_path).set_position('center', 'center')


                if img.size[0] == img.size[1] and res=='tiktok-snapchat':
                    # new_img = img.fx(vfx.resize, height=height-final_top_text_clip.size[1]-final_bottom_text_clip.size[1])
                    new_img = img.fx(vfx.resize, height=height)
                else:
                    if img.size[0] > img.size[1]: 
                        # new_img = img.fx(vfx.resize, height=height-final_top_text_clip.size[1]-final_bottom_text_clip.size[1])
                        new_img = img.fx(vfx.resize, height=height-200)
                    else:
                        new_img = img.fx(vfx.resize, height=height-200)
                        new_img = resize(img, width=width)
                # new_img = new_img.fx(vfx.fadeout, duration=.35)
                # new_img = new_img.fx(transfx.slide_out, duration=.5, side='left')
                if str(img_path_content_type).startswith('video/'):
                    final_duration += new_img.duration 
                elif str(img_path_content_type).startswith('image/'):
                    final_duration += time_per_img
                    new_img = new_img.resize(lambda t: 0.75 + 0.18 * t)  # Zoom-in effect
                    
                clips.append(new_img)





            # Create a video clip from the images using MoviePy
            # clips = [ImageClip(img_path).set_position("center", 'center').fx(vfx.resize, width=width).set_duration(time_per_img) for img_path in image_paths]
            

            # for img in image_paths:
            #     img = ImageClip(img).set_position('center', 'center').fx(vfx.resize, width=width).set_duration(time_per_img) 
            #     new_img = resize(img, height=height)
            #     new_img = new_img.fx(vfx.fadein, duration=.4)
            #     new_img = new_img.fx(transfx.slide_out, duration=.5, side='right')
            #     # new_img = new_img.resize(lambda t: 1 + 0.04 * t)  # Zoom-in effect
            #     clips.append(new_img)


            # for img in image_paths:
            #     img = ImageClip(img).set_position('center', 'center').set_duration(time_per_img)
            #     if img.size[0] == img.size[1] and res=='tiktok-snapchat':
            #         new_img = img.fx(vfx.resize, height=height)
            #     else:
            #         new_img = img.fx(vfx.resize, height=height)
            #         new_img = resize(img, width=width)
            #     # new_img = new_img.fx(vfx.fadeout, duration=.35)
            #     # new_img = new_img.fx(transfx.slide_out, duration=.5, side='left')
            #     new_img = new_img.resize(lambda t: 0.85 + 0.18 * t)  # Zoom-in effect
            #     clips.append(new_img)

            # top_text = arabic_reshaper.reshape(request.POST.get('top_text'))
            top_text = request.POST.get('top_text')
            formated_top_text = []  
            for word in top_text.split(' '):
                formated = reshaper.reshape(word)
                #text_to_display = get_display(formated) 
                formated_top_text.append(formated)

            top_text = get_display(' '.join(formated_top_text) )
             
            
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


            top_text_clip = TextClip(txt=str(top_text), font=font_path ,fontsize=font_size, color='white').set_duration(final_duration)
            bottom_text_clip = TextClip(txt=str(bottom_text), font=font_path ,fontsize=font_size ,color='white').set_duration(final_duration)
            
            top_text_width, top_text_height = top_text_clip.size 
            bottom_text_width, bottom_text_height = bottom_text_clip.size 
            
            top_color_clip = ColorClip(size=(width, top_text_height+20), color=(0, 0, 0)).set_duration(final_duration).set_position("top", "center")
            bottom_color_clip = ColorClip(size=(width, bottom_text_height+20), color=(0, 0, 0)).set_duration(final_duration).set_position("center", "center")

            final_top_text_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip.set_position("center", "center")])
            final_bottom_text_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip.set_position("center", "center")])
            



            watermark = TextClip(txt='Video Editor', font=font_path, fontsize=30).set_opacity(.5).set_position(('center', 'center')).set_duration(time_per_img)

            ## this is final work list
            composite_clips = []

            
            

            if subscription.plan.price == 0: 
                for clip in clips:
                    print('price 0')
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_duration(clip.duration).set_position('top', 'center'), final_bottom_text_clip.set_duration(clip.duration).set_position('bottom', 'center'), watermark], size=(width, height) )
                    # final_composite_clip = CompositeVideoClip([composite_clip, TextClip(txt='Video Editor', font=font_path, fontsize=30).set_position('center', 'center')])
                    composite_clips.append(composite_clip)
            
            else: 
                print("price not 0 ")
                for clip in clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_duration(clip.duration).set_position('top', 'center'), final_bottom_text_clip.set_duration(clip.duration).set_position('bottom', 'center')], size=(width, height))
                    composite_clips.append(composite_clip)




            end_screen = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(time_per_img).set_position("center", "center") 

            end_screen_text = TextClip(txt=end_text, color='white', font=font_path, fontsize=50).set_position(("center", "center")).set_duration(time_per_img) 
            end_screen_url = TextClip(txt=end_url, fontsize=30, color='black', font=font_path).set_duration(time_per_img)
            end_screen_url_color_clip = ColorClip(color=(255, 255, 255), size=(end_screen_url.size[0]+10, end_screen_url.size[1]+20)).set_duration(time_per_img)
            
            end_url_clip = CompositeVideoClip([end_screen_url_color_clip, end_screen_url.set_position(('center', "center"))]) 
            end_url_clip= end_url_clip.fx(transfx.slide_in, duration=1, side='left')

            end_clip = CompositeVideoClip([end_screen, end_screen_text, end_url_clip.set_position(("center", ((height / 2) + 40)))])

            composite_clips.append(end_clip) 


            if request.FILES.get('audio') != None: 
                
                audio = request.FILES.get('audio') 
            
                audio_clip = AudioFileClip(audio.temporary_file_path()) 

                audio_file = afx.audio_loop(audio_clip, duration=(final_duration)) 

                video = concatenate_videoclips(composite_clips, method="chain").set_audio(audio_file)
            else: 

                video = concatenate_videoclips(composite_clips, method="chain")

            # Set the video file name and path
            video_file_name = 'my_video.mp4'
            video_file_path = 'media/' + video_file_name

            # Write the video file to disk
            # video.write_videofile(video_file_path, codec='libx264')
<<<<<<< HEAD

#            video.write_videofile(video_file_path, fps=30)

            video.write_videofile(video_file_path, fps=30)

=======
            video.write_videofile(video_file_path, fps=30, threads=12, codec='libx264')
>>>>>>> 5c2d668830a485702ae5b22e142d84977410a470

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
        return render(request, 'video_v2/create_video.html')

