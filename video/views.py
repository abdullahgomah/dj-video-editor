from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import UploadImageForm, VideoTextForm
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


# Create your views here.



@login_required
def combine_images(request):
    if request.method == 'POST':
        # Get the uploaded images from the HTML form
        time_per_img = int(request.POST.get("time_per_img"))

        images = request.FILES.getlist('images')
        audio = request.FILES.get('audio') 

        audio_clip = AudioFileClip(audio.temporary_file_path()) 

        audio_file = afx.audio_loop(audio_clip, duration=(len(images)* time_per_img))

        res = request.POST.get('video-res') 


        ### color clips here

        width = 0 
        height = 0
        font_size = 20

        if res=='facebook1':
            width = 1200
            height = 628 
        elif res=='facebook2':
            width = 810
            height = 450
        elif res == 'tiktok-snapchat':
            width = 1080
            height = 1920
            font_size = 40 

        # Create a list of image paths
        image_paths = []
        for img in images:
            image_paths.append(img.temporary_file_path())

        # Create a video clip from the images using MoviePy
        clips = [ImageClip(img_path).set_position("center", 'center').fx(vfx.resize, height=height).set_duration(time_per_img) for img_path in image_paths]

        top_text_clip = TextClip(txt=str(request.POST.get("top_text")), fontsize=font_size).set_duration(time_per_img)
        bottom_text_clip = TextClip(txt=str(request.POST.get("bottom_text")), fontsize=font_size ).set_duration(time_per_img)

        ## this is final work list
        composite_clips = []

        for clip in clips:
            composite_clip = CompositeVideoClip([clip, top_text_clip.set_position('top', 'center'), bottom_text_clip.set_position('bottom', 'center')], size=(width, height))
            composite_clips.append(composite_clip)

        video = concatenate_videoclips(composite_clips, method="compose").set_audio(audio_file)

        # Set the video file name and path
        video_file_name = 'my_video.mp4'
        video_file_path = 'media/' + video_file_name

        # Write the video file to disk
        # video.write_videofile(video_file_path, codec='libx264')
        video.write_videofile(video_file_path, fps=24)

        # Open the video file and create an HTTP response with the file contents
        with open(video_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=' + video_file_name

        # Delete the video file from disk
        os.remove(video_file_path)

        return response

    else:
        return render(request, 'video/create_video.html')


@login_required
def remove_audio(request):
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
    if request.method == 'POST':
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
        return response

    return render(request, 'video/change_speed.html')





### إنشاء فيديو مع إضافة لوجو
@login_required
def combine_video_withlogo(request):
    if request.method == 'POST':
        # Get the input files from the HTML form
        images = request.FILES.getlist('image_files')
        audio = request.FILES['audio_file']
        logo = request.FILES['logo_file']
        tpi = request.POST['time_per_img']
        top_text = request.POST['top_text']
        bottom_text = request.POST['bottom_text']

        # Create a random filename for the output video
        filename = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.mp4')

        # Save the logo file to a temporary location
        with open('temp_logo.png', 'wb+') as destination:
            for chunk in logo.chunks():
                destination.write(chunk)

        audio_clip = AudioFileClip(audio.temporary_file_path()) 

        audio_file = afx.audio_loop(AudioFileClip(audio.temporary_file_path()), duration=int(len(images) * int(tpi)))

        res = request.POST.get('video-res') 


        ### color clips here

        width = 0 
        height = 0
        font_size = 20

        if res=='facebook1':
            width = 1200
            height = 628 
        elif res=='facebook2':
            width = 810
            height = 450
        elif res == 'tiktok-snapchat':
            width = 1080
            height = 1920
            font_size = 40 


        image_paths = []
        for img in images:
            image_paths.append(img.temporary_file_path())

        # Create a list of image clips
        # image_clips = [ImageClip(img_path, duration=int(tpi)) for img_path in image_paths]
        image_clips = [ImageClip(img_path).set_position("center", 'center').fx(vfx.resize, height=height).set_duration(tpi) for img_path in image_paths]


        top_text_clip = TextClip(txt=str(request.POST.get("top_text")), fontsize=font_size, size=((0, 0)), color='white').set_duration(tpi)
        bottom_text_clip = TextClip(txt=str(request.POST.get("bottom_text")), fontsize=font_size, size=((0, 0)) ,color='white').set_duration(tpi)
        
        top_text_width, top_text_height = top_text_clip.size 
        bottom_text_width, bottom_text_height = bottom_text_clip.size 
        
        top_color_clip = ColorClip(size=(width, top_text_height+20), color=(0, 0, 0)).set_duration(tpi).set_position("top", "center")
        bottom_color_clip = ColorClip(size=(width, bottom_text_height+20), color=(0, 0, 0)).set_duration(tpi).set_position("center", "center")

        final_top_text_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip.set_position("center", "center")])
        final_bottom_text_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip.set_position("center", "center")])

        ## this is final clips list
        composite_clips = []

        for clip in image_clips:
            composite_clip = CompositeVideoClip([clip, final_top_text_clip.set_position('top', 'center'), final_bottom_text_clip.set_position('bottom', 'center')], size=(width, height))
            composite_clips.append(composite_clip)


        # Concatenate the image clips into a video clip
        video_clip = concatenate_videoclips(composite_clips, method='compose').set_audio(audio_file)


        # Load the logo image using moviepy
        logo_clip = ImageClip('temp_logo.png', transparent=True).set_duration(video_clip.duration).resize(height=110)

        # Add the logo to the video clip
        video_clip = CompositeVideoClip([video_clip, logo_clip.set_position(('left', 'top'))])

        # Save the final video to the output file
        video_clip.write_videofile(filename, fps=25)

        # Serve the video file for download
        with open(filename, 'rb') as video:
            response = HttpResponse(video.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename=output_video.mp4'

        # Delete the temporary files
        os.remove(filename)
        os.remove('temp_logo.png')

        return response

    return render(request, 'video/combine_video_withlogo.html')





# هنا نموذج الفيديو الثالث

@login_required
def feedback_video_template(request):

    if request.method == 'POST': 

        video = request.FILES['video']
        background = request.FILES['background']
        text = request.POST['text']
        res = request.POST.get('video-res') 
        fontsize = request.POST.get('fontsize')

        video = VideoFileClip(video.temporary_file_path())
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


        ## Text Clip Here 
        text_clip = TextClip(txt=text, fontsize=int(fontsize), color='gold').set_duration(video.duration).set_position('right', 'center')



        img = ImageClip(background.temporary_file_path(), duration=duration)

        # Resized Image
        resized = resize(img, width=width) 
        r_width, r_height = resized.size 

        maskclip=ImageClip("mask1.png",ismask=True).set_duration(duration) 
        m_width, m_height = maskclip.size 


        # Resized Video 
        resized_video = resize(video.set_position(("center", "center")), height=m_height)

        resized_video = resized_video.set_mask(maskclip)

        # top_text_clip = TextClip(txt="Ramadan Kareem", fontsize=20, color='white', size=((0, 0))).set_duration(duration).set_position('center', 'center')
        # bottom_text_clip = TextClip(txt="Amazing Sales in Ramadan", fontsize=20, color='white', size=((0, 0))).set_duration(duration).set_position('center', 'center')

        # t_text_width, t_text_height = top_text_clip.size 


        # top_color_clip = ColorClip(size=(r_width, t_text_height+20), color=(0, 0, 0)).set_duration(duration).set_position("top", "center")
        # bottom_color_clip = ColorClip(size=(r_width, t_text_height+20), color=(0, 0, 0)).set_duration(duration).set_position("center", "center")


        # top_text_work_clip = CompositeVideoClip(clips=[top_color_clip, top_text_clip])
        # bottom_text_work_clip = CompositeVideoClip(clips=[bottom_color_clip, bottom_text_clip])

        # part1 = CompositeVideoClip(clips=[resized, top_text_work_clip])

        # part2 = CompositeVideoClip([part1, bottom_text_work_clip.set_position("bottom", "center")])

        final = CompositeVideoClip([img, resized_video.set_position((100, 'center'))], size=(width, height))
        final2 = CompositeVideoClip([final, text_clip.set_position(((r_width - 100), 'center'))], size=(width, height)) 

    
        # top_text_work_clip.save_frame('out.png')

        final2.write_videofile("out.mp4", fps=25)

        ## DOWNLOAD FILE
        with open('out.mp4', 'rb') as video:
            response = HttpResponse(video.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename=output_video.mp4'

        # Delete the temporary files
        os.remove('out.mp4')

        return response

    return render(request, 'video/create_feedback_video.html', {})