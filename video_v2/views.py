
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import redirect, render 
from moviepy.editor import *
from moviepy.editor import transfx, vfx
from moviepy.video.fx.resize import resize
from django.contrib.auth.decorators import login_required

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


def hex_to_rgb(hex_color):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Extract individual color components
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    return (red, green, blue)


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
            font_size_input = request.POST.get('font-size-input') 
            bg_color_input = request.POST.get('bg-color-inoput') 
            font_color_input= request.POST.get('font-color-input')
            bg_rgb_color = hex_to_rgb(bg_color_input) 
            font_rgb_color = hex_to_rgb(font_color_input) 

            top_text_input_2 = "" 
            if request.POST.get('top-text-input-2') != "" or request.POST.get('top-text-input-2') != None: 
                top_text_input_2 = request.POST.get('top-text-input-2') 
                
            top_text_input_3 = "" 
            if request.POST.get('top-text-input-3') != "" or request.POST.get('top-text-input-3') != None: 
                top_text_input_3 = request.POST.get('top-text-input-3') 

            top_text_input_4 = "" 
            if request.POST.get('top-text-input-4') != "" or request.POST.get('top-text-input-4') != None: 
                top_text_input_4 = request.POST.get('top-text-input-4') 
                

            print(bg_color_input) 

            final_duration = 0 

            images = request.FILES.getlist('images')
            

            widths_list = [] 
            heights_list = [] 


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
            try: 
                font_size = int(font_size_input)
            except: 
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
                    img = VideoFileClip(img_path).set_position(('center', 'center'))
    
                

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
                        
                transition_select= request.POST.get('transition-input') 



                if str(img_path_content_type).startswith('video/'):
                    final_duration += new_img.duration 
                elif str(img_path_content_type).startswith('image/'):
                    final_duration += time_per_img
                    new_img = new_img.resize(lambda t: 0.75 + 0.18 * t)  # Zoom-in effect
                    
                clips.append(new_img)
                widths_list.append(new_img.size[0])
                heights_list.append(new_img.size[1])



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


            top_text_clip = TextClip(txt=str(top_text), font=font_path ,fontsize=font_size, color=font_color_input).set_duration(final_duration)
            bottom_text_clip = TextClip(txt=str(bottom_text), font=font_path ,fontsize=font_size ,color=font_color_input).set_duration(final_duration)
            
            top_text_width, top_text_height = top_text_clip.size 
            bottom_text_width, bottom_text_height = bottom_text_clip.size 
            
            top_color_clip = ColorClip(size=(width, top_text_height+20), color=bg_rgb_color).set_duration(final_duration).set_position("top", "center")
            bottom_color_clip = ColorClip(size=(width, bottom_text_height+20), color=bg_rgb_color).set_duration(final_duration).set_position("center", "center")

            final_top_text_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip.set_position("center", "center")])
            final_bottom_text_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip.set_position("center", "center")])
            



            watermark = TextClip(txt='Video Editor', font=font_path, fontsize=30).set_opacity(.5).set_position(('center', 'center')).set_duration(time_per_img)

            ## this is final work list
            composite_clips = []

            
            

            if subscription.plan.price == 0: 
                for clip in clips:
                    print('price 0')
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_duration(clip.duration).set_position('top', 'center'), final_bottom_text_clip.set_duration(clip.duration).set_position('bottom', 'center'), watermark], size=(width, (height )) )
                    # final_composite_clip = CompositeVideoClip([composite_clip, TextClip(txt='Video Editor', font=font_path, fontsize=30).set_position('center', 'center')])
                    composite_clips.append(composite_clip)
            
            else: 
                print("price not 0 ")
                for clip in clips:
                    composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_duration(clip.duration).set_position('top', 'center'), final_bottom_text_clip.set_duration(clip.duration).set_position('bottom', 'center')], size=(width, (height )))
                    composite_clips.append(composite_clip)




            end_screen = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(time_per_img).set_position("center", "center") 

            end_screen_text = TextClip(txt=end_text, color='white', font=font_path, fontsize=50).set_position(("center", "center")).set_duration(time_per_img) 
            end_screen_url = TextClip(txt=end_url, fontsize=30, color='black', font=font_path).set_duration(time_per_img)
            end_screen_url_color_clip = ColorClip(color=(255, 255, 255), size=(end_screen_url.size[0]+10, end_screen_url.size[1]+20)).set_duration(time_per_img)
            
            end_url_clip = CompositeVideoClip([end_screen_url_color_clip, end_screen_url.set_position(('center', "center"))]) 
            end_url_clip= end_url_clip.fx(transfx.slide_in, duration=1, side='left')

            end_clip = CompositeVideoClip([end_screen, end_screen_text, end_url_clip.set_position(("center", ((height / 2) + 30)))])

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

#            video.write_videofile(video_file_path, fps=30)

#            video.write_videofile(video_file_path, fps=30)

            video.write_videofile(video_file_path, fps=30, threads=12, codec='libx264')

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



def combine_imgs_v2(request): 
    if request.POST: 
        top_text = request.POST.get('top-text')
        bottom_text = request.POST.get('bottom-text')

        """
        هنا انا بفكر ازاي هحسب العرض بتاع النص العلوي والسفلي واخلي النص ميعديش العرض بتاع الشاشة نفسها 
        عشان اعمل لون الخلفية 
        بعدين عاوز اعمل input 
        للخلفية عشان المستخدم يقدر يغير لون الخلفية زي ما هو عايز
        بعدها عاوز اعرف ايه وحدة قياس حجم الخط عشان اسمح للمستخدم يغيره برضو عن طريق input 
        بعدها عاوز ابحث في الانتقالات بين الكليبات وخليها عشوائية أو الأفضل من كده اني اخلي المستخدم يختار التنقل في المشروع بتاعه
        كمان عاوز ما انساش احول الكلام زي الدالة اللي فوق دي عشان ما يحصلش مشكلة في الكلام العربي 
        عاوز اعمل العلامة المائية برضو بس بطريقة أحسن 
        """

        widths_list = [] 
        heights_list = [] 
        clips = [] 
        final_clips = [] 
        tpi = request.POST.get('tpi')
        imgs = request.FILES.getlist('imgs-input') 
        for img in imgs: 
            img_path = img.temporary_file_path() 
            img_content_type = img.content_type 
            if img_content_type.startswith('video/'): 
                img = VideoFileClip(img_path).set_position(('center', 'center')) 
                if float(img.fps == 90000):
                    continue 
            else: 
                img = ImageClip(img_path).set_duration(tpi).set_position(('center', 'center'))

            img_width = img.size[0] 
            img_height = img.size[1] 

            widths_list.append(img_width) 
            heights_list.append(img_height)

            clips.append(img) 

        
        for clip in clips: 
            clip = CompositeVideoClip(clips=[clip.set_position(('center', 'center'))], size=((int(max(widths_list)), int(max(heights_list))))) 
            final_clips.append(clip) 


        video = concatenate_videoclips(final_clips, method="chain")
        video_file_name = 'my_video.mp4'
        video_file_path = 'media/' + video_file_name
        
        video.write_videofile(video_file_path, fps=30, threads=12, codec='libx264')

        # Open the video file and create an HTTP response with the file contents
        with open(video_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + video_file_name

        # Delete the video file from disk
        os.remove(video_file_path)
        
        return response 




    context = {} 
    return render(request, 'video_v2/combine-v2.html', context)



def return_rgb(color): 
    r= int(color[1:3], 16)
    g= int(color[3:5], 16)
    b= int(color[5:7], 16)

    return r,g,b


def create_text_clip(txt, font_color, bg_color, font_size): 
    clip = TextClip(txt, color=font_color, bg_color=bg_color, fontsize=font_size)
    return clip 


def text_preview_export(request):

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



    if request.POST: 

        print("LOGO INPUT") 
        logo_input_file = request.FILES.get('logo-input')
        print(logo_input_file)
        print("#"* 50) 


        if subscription.videos_per_months != 0:


            audio_input = request.FILES.get('audio-input')
            audio_clip = None 


            resize_files_input = request.POST.get('resize-files-input') 

            if audio_input != None: 
                audio_content_type = audio_input.content_type 
                audio_path = audio_input.temporary_file_path() 

                if str(audio_content_type).startswith('audio/'): 
                    audio_clip = AudioFileClip(audio_path) 
                elif str(audio_content_type).startswith('video/'): 
                    audio_clip = VideoFileClip(audio_path).audio 

        
            
            font_size_input = request.POST.get('font-size-input') 

            
            if font_size_input != None or font_size_input != '': 
                try:
                    font_size_input = int(font_size_input) 
                except: 
                    font_size_input = 20 ## Default
            else: 
                font_size_input = 20


            opacity_input = request.POST.get('opacity-input') 

            if opacity_input != None or opacity_input != "": 
                try: 
                    opacity_input = float(opacity_input) 
                except: 
                    opacity_input = .75
            else: 
                opacity_input = 0.75

            end_screen_main_text = request.POST.get('end-screen-main-txt') 
            end_screen_url_text = request.POST.get('end-screen-url-txt')
            end_screen_bg = request.POST.get('end-scrren-bg')
            end_screen_fg = request.POST.get('end-scrren-fg') 

            if end_screen_bg != None or end_screen_bg != "": 
                end_screen_bg = return_rgb(end_screen_bg)


            res = request.POST.get('video-res') 
            transition = request.POST.get('transition-select')
            tpi_input = request.POST.get('tpi-input') 
            if tpi_input == "" or tpi_input == 0 or tpi_input == None: 
                tpi_input = 5
            total_duration = 0 
            clips = [] 
            width, height= 1080, 1080
            if res == 'facebook1': 
                width = 1200 
                height = 628  
            elif res == 'facebook2': 
                width = 810 
                height  =  450  
            elif res == 'tiktok-snapchat': 
                width = 1080 
                height = 1920 
            elif res == 'square': 
                width = 1080 
                height = 1080 


            ## Start End Screen Creation 
            end_screen_bg_layer = ColorClip(size=((width, height)), color=end_screen_bg).set_position("center", "center").set_duration(4) 
            if end_screen_main_text != None or str(end_screen_main_text).strip() == "": 
                end_screen_main_text_layer = TextClip(txt=end_screen_main_text, color=end_screen_fg, method='caption', font=font_path, align='center', size=((width, 0)), fontsize=int(font_size_input)).set_duration(4).set_position('center', 'center') 
            
            if end_screen_url_text != None or str(end_screen_url_text).strip() == "": 
                end_screen_url_text_layer = TextClip(txt=end_screen_url_text, color=end_screen_fg, method='caption',font=font_path, fontsize=int(font_size_input)).set_duration(4) 
                end_screen_url_text_layer = end_screen_url_text_layer.set_position(('center', ((height / 2) + end_screen_main_text_layer.size[1]+ 20)))
            
            final_end_screen = CompositeVideoClip([end_screen_bg_layer, end_screen_main_text_layer, end_screen_url_text_layer])


            top_text_1 = request.POST.get('top-text-input-1') 
            top_text_2 = request.POST.get('top-text-input-2') 
            top_text_3 = request.POST.get('top-text-input-3') 
            top_text_4 = request.POST.get('top-text-input-4')

            bottom_text_1 = request.POST.get('bottom-text-input-1') 
            bottom_text_2 = request.POST.get('bottom-text-input-2') 
            bottom_text_3 = request.POST.get('bottom-text-input-3') 
            bottom_text_4 = request.POST.get('bottom-text-input-4') 

            top_text_list = [top_text_1, top_text_2, top_text_3, top_text_4]
            bottom_text_list = [bottom_text_1, bottom_text_2, bottom_text_3, bottom_text_4]
            new_top_text_list = [] 
            new_bottom_text_list = [] 

            ## error happen becacuse list decreases, I should solve it using new list to add the value to it 
            for i in range(int(len(top_text_list))): 
                print(top_text_list[i]) 
                if top_text_list[i] != None or top_text_list[i] != "" or top_text_list[i] != " " or len(top_text_list[i]) != 0: 
                    formated_top_text = []  
                    for word in top_text_list[i].split(' '):
                        formated = reshaper.reshape(word)
                        text_to_display = get_display(formated)
                        # formated_top_text.append(formated)
                        formated_top_text.append(text_to_display)

                    top_text = get_display(' '.join(formated_top_text) )
                    # top_text = ' '.join(formated_top_text)
                
                    new_top_text_list.append(top_text) 
            
            for i in range(int(len(bottom_text_list))): 
                formated_top_text = []  
                for word in bottom_text_list[i].split(' '):
                    formated = reshaper.reshape(word)
                    text_to_display = get_display(formated) 
                    # formated_top_text.append(formated)
                    formated_top_text.append(text_to_display)

                bottom_text = get_display(' '.join(formated_top_text) )
                # bottom_text = ' '.join(formated_top_text) 
                
                new_bottom_text_list.append(bottom_text) 
            
            
            """
            المفروض هنا هعمل كليب نصي لكل عنصر من اللي موجودين في القائمة
            احتساب الوقت هيكون كالتالي
            هناخد الوقت الكلي للفيديو 
            بعدين هنقسم على عدد النصوص الموجودة الغير فارغة 
            وبكده تكون كملن ان شاء الله 🚀
            """
            
            top_clips = []
            bottom_clips = [] 

            
            files = request.FILES.getlist('images-input')
            for file in files: 
                file_path =file.temporary_file_path() 
                file_content_type = file.content_type 
                
                if str(file_content_type).startswith('video/'): 
                    clip = VideoFileClip(file_path)
                elif str(file_content_type).startswith('image/'): 
                    clip = ImageClip(file_path).set_duration(tpi_input) 
                
                
                if resize_files_input == 'on': 
                    # if clip.size[0] > clip.size[1]: 
                    #     clip = resize(clip, height=height) 
                    # else: 
                    #     clip = resize(clip, width=width) 
                    # clip = resize(clip, width=width) 
                    clip = clip.fx(vfx.resize, width=width)
                    # if clip.size[0] > width * 1.1:  # Adjust as necessary
                    #     clip = resize(clip, width=width)  # Maintains aspect ratio
                
                clip = CompositeVideoClip([clip.set_position('center', 'center')], size=((width, height)))

                if transition == 'fade_in': 
                    clip = transfx.fadein(clip, 1) 
                elif transition == 'fade_out': 
                    clip = transfx.fadeout(clip, 1) 
                elif transition == 'slide_in': 
                    clip = CompositeVideoClip([transfx.slide_in(clip, 1, 'left')])
                elif transition == 'slide_out': 
                    clip = CompositeVideoClip([transfx.slide_out(clip, 1, 'left')])
                
                total_duration += clip.duration
                clip = clip.set_position('center', 'center') 
                if clip.fps != 90000: 
                    clips.append(clip)  
            
            print('TOTOAL DURATION') 
            print(total_duration) 
            print('=======') 

            text_color = request.POST.get('text-color-input') 
            bg_color = request.POST.get('bg-color-input') 
            if bg_color != None or bg_color != "": 
                bg_color = return_rgb(bg_color)

            tpt =total_duration / len(clips) 
            top_tpt = total_duration / len(new_top_text_list) 
            bottom_tpt = total_duration / len(new_bottom_text_list) 
            last_end = 0 

            print('TPT') 
            print(tpt) 
            print('================')


            final = concatenate_videoclips(clips=clips, method='chain') 
            final = CompositeVideoClip([final.set_position(('center','center'))], size=((width, height)), bg_color=bg_color)


            # for txt in new_top_text_list: 
            for txt in top_text_list: 
                if txt == "" or str(txt).strip() == "":
                    continue ### اسطوووري 
                clip = TextClip(txt, fontsize=font_size_input, color=text_color, method='caption', size=((final.size[0],0)), font=new_font)
                clip = clip.set_duration(top_tpt)
                clip = clip.set_position(('center','center')) 
                color_clip = ColorClip(size=((width, clip.size[1]+20)), color=bg_color).set_duration(clip.duration).set_opacity(opacity_input)
                clip = CompositeVideoClip([color_clip, clip]).set_position('center','top')
                clip = clip.set_start(last_end) 
                end = top_tpt + last_end
                clip = clip.set_end(end) 
                last_end = end 

                top_clips.append(clip) 

            last_end = 0 
            end = 0 
            print('new bottom text list')
            print(new_bottom_text_list)
            print('#' * 30) 
            # for txt in new_bottom_text_list: 
            for txt in bottom_text_list: 
                if txt == "" or str(txt).strip() == "":
                    continue ### اسطوووري 
                clip = TextClip(txt, fontsize=font_size_input, color=text_color, method='caption', size=((final.size[0],0)), font=new_font)
                clip = clip.set_duration(bottom_tpt)
                clip = clip.set_position(('center','center')) 
                color_clip = ColorClip(size=((width, clip.size[1]+20)), color=bg_color).set_duration(clip.duration).set_opacity(opacity_input)
                clip = CompositeVideoClip([color_clip, clip]).set_position('center','bottom')
                clip = clip.set_start(last_end) 
                end = bottom_tpt + last_end
                clip = clip.set_end(end) 
                last_end = end 

                bottom_clips.append(clip) 

            top_text_final = concatenate_videoclips(top_clips, method='chain') 
            bottom_final_text = concatenate_videoclips(bottom_clips, method='chain')
            final = CompositeVideoClip(clips=[final, top_text_final, bottom_final_text.set_position('bottom')])
            final = concatenate_videoclips([final, final_end_screen], method='chain')

            if audio_clip != None: 

                final = final.without_audio() 
                print('final duration: '+str(final.duration))
                print("this is audio_clip duration: "+str(audio_clip.duration))
                if audio_clip.duration > final.duration: 
                    print('audio_clip.duration>final.duration')
                    audio_clip = audio_clip.set_start(0).set_end(final.duration) 
                elif audio_clip.duration < final.duration: 
                    print('audio_clip.duration < final.duration' )
                    if request.POST.get('loop-audio-input') == 1: 
                        print(request.POST.get('loop-audio-input'))
                        audio_clip = afx.audio_loop(audio_clip, duration=int(final.duration)) 
                    else: 
                        audio_clip = audio_clip.set_start(0).set_end(final.duration) 
                final = final.set_audio(audio_clip) 

            

            if logo_input_file != None or logo_input_file != "": 
                logo_input_path = logo_input_file.temporary_file_path() 
                logo_clip = ImageClip(logo_input_path).set_duration(final.duration) 
                logo_clip = resize(logo_clip, width=200) 
                # logo_clip = logo_clip.set_position("left", "top")  

                final  = CompositeVideoClip([final, logo_clip.set_position("left", "top")])
            

            # final.write_videofile('output.mp4', fps=30, threads=12, codec='libx264')
            print('THIS IS DURATION') 
            print(final.duration)
            if final.duration > 6: 
                final.set_end(6).write_videofile('output.mp4', fps=30, threads=12, preset='ultrafast') 
            else: 
                final.write_videofile('output.mp4', fps=30, threads=12, preset='ultrafast') 

            with open('output.mp4', 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4') 
                response['Content-Disposition'] = 'attachment; filename=' + 'output.mp4'

            os.remove('output.mp4') 
            subscription.videos_per_months -= 1 
            subscription.save() 


            return response 
        else: 
            subscription.delete() 
            return redirect('/pay/limit_ended/')




    context = {} 
    return render(request, 'video_v2/new_create.html', context)



@login_required
def new_create(request): 


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


    if request.POST: 

        print("LOGO INPUT") 
        logo_input_file = request.FILES.get('logo-input')
        print(logo_input_file)
        print("#"* 50) 

        if subscription.videos_per_months != 0:


            audio_input = request.FILES.get('audio-input')
            audio_clip = None 


            resize_files_input = request.POST.get('resize-files-input') 

            if audio_input != None: 
                audio_content_type = audio_input.content_type 
                audio_path = audio_input.temporary_file_path() 

                if str(audio_content_type).startswith('audio/'): 
                    audio_clip = AudioFileClip(audio_path) 
                elif str(audio_content_type).startswith('video/'): 
                    audio_clip = VideoFileClip(audio_path).audio 

        
            
            font_size_input = request.POST.get('font-size-input') 

            
            if font_size_input != None or font_size_input != '': 
                try:
                    font_size_input = int(font_size_input) 
                except: 
                    font_size_input = 20 ## Default
            else: 
                font_size_input = 20


            opacity_input = request.POST.get('opacity-input') 

            if opacity_input != None or opacity_input != "": 
                try: 
                    opacity_input = float(opacity_input) 
                except: 
                    opacity_input = .75
            else: 
                opacity_input = 0.75

            end_screen_main_text = request.POST.get('end-screen-main-txt') 
            end_screen_url_text = request.POST.get('end-screen-url-txt')
            end_screen_bg = request.POST.get('end-scrren-bg')
            end_screen_fg = request.POST.get('end-scrren-fg') 

            if end_screen_bg != None or end_screen_bg != "": 
                end_screen_bg = return_rgb(end_screen_bg)


            res = request.POST.get('video-res') 
            transition = request.POST.get('transition-select')
            tpi_input = request.POST.get('tpi-input') 
            if tpi_input == "" or tpi_input == 0 or tpi_input == None: 
                tpi_input = 5
            total_duration = 0 
            clips = [] 
            width, height= 1080, 1080
            if res == 'facebook1': 
                width = 1200 
                height = 628  
            elif res == 'facebook2': 
                width = 810 
                height  =  450  
            elif res == 'tiktok-snapchat': 
                width = 1080 
                height = 1920 
            elif res == 'square': 
                width = 1080 
                height = 1080 


            ## Start End Screen Creation 
            end_screen_bg_layer = ColorClip(size=((width, height)), color=end_screen_bg).set_position("center", "center").set_duration(4) 
            if end_screen_main_text != None or str(end_screen_main_text).strip() == "": 
                end_screen_main_text_layer = TextClip(txt=end_screen_main_text, color=end_screen_fg, method='caption', font=font_path, align='center', size=((width, 0)), fontsize=int(font_size_input)).set_duration(4).set_position('center', 'center') 
            
            if end_screen_url_text != None or str(end_screen_url_text).strip() == "": 
                end_screen_url_text_layer = TextClip(txt=end_screen_url_text, color=end_screen_fg, method='caption',font=font_path, fontsize=int(font_size_input)).set_duration(4) 
                end_screen_url_text_layer = end_screen_url_text_layer.set_position(('center', ((height / 2) + end_screen_main_text_layer.size[1]+ 20)))
            
            final_end_screen = CompositeVideoClip([end_screen_bg_layer, end_screen_main_text_layer, end_screen_url_text_layer])


            top_text_1 = request.POST.get('top-text-input-1') 
            top_text_2 = request.POST.get('top-text-input-2') 
            top_text_3 = request.POST.get('top-text-input-3') 
            top_text_4 = request.POST.get('top-text-input-4')

            bottom_text_1 = request.POST.get('bottom-text-input-1') 
            bottom_text_2 = request.POST.get('bottom-text-input-2') 
            bottom_text_3 = request.POST.get('bottom-text-input-3') 
            bottom_text_4 = request.POST.get('bottom-text-input-4') 

            top_text_list = [top_text_1, top_text_2, top_text_3, top_text_4]
            bottom_text_list = [bottom_text_1, bottom_text_2, bottom_text_3, bottom_text_4]
            new_top_text_list = [] 
            new_bottom_text_list = [] 

            ## error happen becacuse list decreases, I should solve it using new list to add the value to it 
            for i in range(int(len(top_text_list))): 
                print(top_text_list[i]) 
                if top_text_list[i] != None or top_text_list[i] != "" or top_text_list[i] != " " or len(top_text_list[i]) != 0: 
                    formated_top_text = []  
                    for word in top_text_list[i].split(' '):
                        formated = reshaper.reshape(word)
                        text_to_display = get_display(formated)
                        # formated_top_text.append(formated)
                        formated_top_text.append(text_to_display)

                    top_text = get_display(' '.join(formated_top_text) )
                    # top_text = ' '.join(formated_top_text)
                
                    new_top_text_list.append(top_text) 
            
            for i in range(int(len(bottom_text_list))): 
                formated_top_text = []  
                for word in bottom_text_list[i].split(' '):
                    formated = reshaper.reshape(word)
                    text_to_display = get_display(formated) 
                    # formated_top_text.append(formated)
                    formated_top_text.append(text_to_display)

                bottom_text = get_display(' '.join(formated_top_text) )
                # bottom_text = ' '.join(formated_top_text) 
                
                new_bottom_text_list.append(bottom_text) 
            
            
            """
            المفروض هنا هعمل كليب نصي لكل عنصر من اللي موجودين في القائمة
            احتساب الوقت هيكون كالتالي
            هناخد الوقت الكلي للفيديو 
            بعدين هنقسم على عدد النصوص الموجودة الغير فارغة 
            وبكده تكون كملن ان شاء الله 🚀
            """
            
            top_clips = []
            bottom_clips = [] 

            
            files = request.FILES.getlist('images-input')
            for file in files: 
                file_path =file.temporary_file_path() 
                file_content_type = file.content_type 
                
                if str(file_content_type).startswith('video/'): 
                    clip = VideoFileClip(file_path)
                elif str(file_content_type).startswith('image/'): 
                    clip = ImageClip(file_path).set_duration(tpi_input) 
                
                
                if resize_files_input == 'on': 
                    # if clip.size[0] > clip.size[1]: 
                    #     clip = resize(clip, height=height) 
                    # else: 
                    #     clip = resize(clip, width=width) 
                    # clip = resize(clip, width=width) 
                    clip = clip.fx(vfx.resize, width=width)
                    # if clip.size[0] > width * 1.1:  # Adjust as necessary
                    #     clip = resize(clip, width=width)  # Maintains aspect ratio
                
                clip = CompositeVideoClip([clip.set_position('center', 'center')], size=((width, height)))

                if transition == 'fade_in': 
                    clip = transfx.fadein(clip, 1) 
                elif transition == 'fade_out': 
                    clip = transfx.fadeout(clip, 1) 
                elif transition == 'slide_in': 
                    clip = CompositeVideoClip([transfx.slide_in(clip, 1, 'left')])
                elif transition == 'slide_out': 
                    clip = CompositeVideoClip([transfx.slide_out(clip, 1, 'left')])
                
                total_duration += clip.duration
                clip = clip.set_position('center', 'center') 
                if clip.fps != 90000: 
                    clips.append(clip)  
            
            print('TOTOAL DURATION') 
            print(total_duration) 
            print('=======') 

            text_color = request.POST.get('text-color-input') 
            bg_color = request.POST.get('bg-color-input') 
            if bg_color != None or bg_color != "": 
                bg_color = return_rgb(bg_color)

            tpt =total_duration / len(clips) 
            top_tpt = total_duration / len(new_top_text_list) 
            bottom_tpt = total_duration / len(new_bottom_text_list) 
            last_end = 0 

            print('TPT') 
            print(tpt) 
            print('================')


            final = concatenate_videoclips(clips=clips, method='chain') 
            final = CompositeVideoClip([final.set_position(('center','center'))], size=((width, height)), bg_color=bg_color)


            # for txt in new_top_text_list: 
            for txt in top_text_list: 
                if txt == "" or str(txt).strip() == "":
                    continue ### اسطوووري 
                clip = TextClip(txt, fontsize=font_size_input, color=text_color, method='caption', size=((final.size[0],0)), font=new_font)
                clip = clip.set_duration(top_tpt)
                clip = clip.set_position(('center','center')) 
                color_clip = ColorClip(size=((width, clip.size[1]+20)), color=bg_color).set_duration(clip.duration).set_opacity(opacity_input)
                clip = CompositeVideoClip([color_clip, clip]).set_position('center','top')
                clip = clip.set_start(last_end) 
                end = top_tpt + last_end
                clip = clip.set_end(end) 
                last_end = end 

                top_clips.append(clip) 

            last_end = 0 
            end = 0 
            print('new bottom text list')
            print(new_bottom_text_list)
            print('#' * 30) 
            # for txt in new_bottom_text_list: 
            for txt in bottom_text_list: 
                if txt == "" or str(txt).strip() == "":
                    continue ### اسطوووري 
                clip = TextClip(txt, fontsize=font_size_input, color=text_color, method='caption', size=((final.size[0],0)), font=new_font)
                clip = clip.set_duration(bottom_tpt)
                clip = clip.set_position(('center','center')) 
                color_clip = ColorClip(size=((width, clip.size[1]+20)), color=bg_color).set_duration(clip.duration).set_opacity(opacity_input)
                clip = CompositeVideoClip([color_clip, clip]).set_position('center','bottom')
                clip = clip.set_start(last_end) 
                end = bottom_tpt + last_end
                clip = clip.set_end(end) 
                last_end = end 

                bottom_clips.append(clip) 

            top_text_final = concatenate_videoclips(top_clips, method='chain') 
            bottom_final_text = concatenate_videoclips(bottom_clips, method='chain')
            final = CompositeVideoClip(clips=[final, top_text_final, bottom_final_text.set_position('bottom')])
            final = concatenate_videoclips([final, final_end_screen], method='chain')

            if audio_clip != None: 
                
                print('loop-audio-input')
                print(request.POST.get('loop-audio-input'))
                print('#########')


                final = final.without_audio() 
                print('final duration: '+str(final.duration))
                print("this is audio_clip duration: "+str(audio_clip.duration))
                if audio_clip.duration > final.duration: 
                    print('audio_clip.duration>final.duration')
                    audio_clip = audio_clip.set_start(0).set_end(final.duration) 
                elif audio_clip.duration < final.duration: 
                    print('audio_clip.duration < final.duration' )
                    if request.POST.get('loop-audio-input') =="on": 
                        # audio_clip = afx.audio_loop(audio_clip, duration=int(final.duration)) 
                        audio_clip = afx.audio_loop(audio_clip, duration=final.duration ) 
                    #else: 
                    #    audio_clip = audio_clip.set_start(0).set_end(final.duration) 
                final = final.set_audio(audio_clip) 

            # final.write_videofile('output.mp4', fps=30, threads=12, codec='libx264')

            if logo_input_file != None or logo_input_file != "": 
                logo_input_path = logo_input_file.temporary_file_path() 
                logo_clip = ImageClip(logo_input_path).set_duration(final.duration) 
                logo_clip = logo_clip.set_position('top', 'left') 

                final  = CompositeVideoClip([final, logo_clip])
            
            final.write_videofile('output.mp4', fps=30, threads=12, preset='ultrafast') 

            with open('output.mp4', 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4') 
                response['Content-Disposition'] = 'attachment; filename=' + 'output.mp4'

            os.remove('output.mp4') 
            subscription.videos_per_months -= 1 
            subscription.save() 


            return response 
        else: 
            subscription.delete() 
            return redirect('/pay/limit_ended/')




    context = {} 
    return render(request, 'video_v2/new_create.html', context)


import os
import subprocess
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Consider handling CSRF properly in production
def upload_and_create_video_with_ffmpeg(request):
    if request.method == 'POST':
        images = request.FILES.getlist('files-input')
        if images:
            image_paths = []
            for i, image in enumerate(images):
                # Save each image to MEDIA_ROOT and collect their paths
                # Ensure images are named sequentially to maintain order
                filename = f"{i:03d}_{image.name}"
                path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                image_paths.append(path)

            # Generate a file listing all image paths
            filelist_path = os.path.join(settings.MEDIA_ROOT, 'filelist.txt')
            with open(filelist_path, 'w', encoding='utf-8') as filelist:
                for path in image_paths:
                    filelist.write(f"file '{path}'\n")
                    filelist.write(f"duration 4\n")
            
            # Exclude duration for the last image to avoid a duplicate frame issue
            with open(filelist_path, 'a', encoding='utf-8') as filelist:
                filelist.write(f"file '{image_paths[-1]}'\n")
            
            # Use ffmpeg to create a video from the images
            video_path = os.path.join(settings.MEDIA_ROOT, 'output.mp4')
            ffmpeg_cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', filelist_path,
                '-vsync', 'vfr', '-pix_fmt', 'yuv420p', '-r', '30', video_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            
            # Serve video file for download
            with open(video_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="output.mp4"'
                return response
        else:
            return HttpResponse("No images were uploaded.", status=400)
    else:
        return render(request, 'upload_form.html')