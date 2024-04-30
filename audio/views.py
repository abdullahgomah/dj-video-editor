from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os 
from moviepy.editor import * 
from pydub import AudioSegment
from pay.models import Subscription, Plan, Feature 
import datetime 

# Create your views here.


# AudioSegment.ffmpeg = '/usr/local/bin/ffmpeg' 
# AudioSegment.converter = '/usr/local/bin/ffmpeg'



@login_required
def change_audio_speed(request):

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

    if features.change_audio_speed == True:
        pass 
    else: 
        return redirect('/pay/plans/')

    if request.method == 'POST':


        audio_file = request.FILES['audio_file']
        speed_factor = float(request.POST['speed_factor'])

        # Save the uploaded audio file to a temporary file
        # with open('temp_audio.mp3', 'wb+') as destination:
        #     for chunk in audio_file.chunks():
        #         destination.write(chunk)

 
        # Open the audio file with PyDub
        audio_segment = AudioSegment.from_file_using_temporary_files(audio_file)

        # Change the speed of the audio
        new_audio_segment = audio_segment.speedup(speed_factor)

        # Save the new audio to a file
        new_filename = 'modified_audio.mp3'
        new_audio_segment.export(new_filename, format='mp3', codec='mp3')

        # Serve the new audio for download
        with open(new_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(new_filename))
        
        os.remove(new_filename)
            
        return response
        
    return render(request, 'audio/changespeed.html')



@login_required
def download_audio(request): 
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


    if features.change_audio_speed == True:
        pass 
    else: 
        return redirect('/pay/plans/')


    if request.method == 'POST' and request.FILES['video']:
        # Get the uploaded video file from the HTML input
        video_file = request.FILES['video']

        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')

        # Save the video file to a temporary location
        with open('temp_video.mp4', 'wb+') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # Load the video file using moviepy
        video_clip = VideoFileClip('temp_video.mp4')

        # Extract the audio from the video clip
        audio_clip = video_clip.audio

        # Save the audio to a file
        audio_clip.write_audiofile('audio.mp3') 

        # Clean up the temporary video file

        # Serve the audio file to the user for download
        with open('audio.mp3', 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

        # os.remove('temp_video.mp4')
        return response

    return render(request, 'audio/download_audio.html')