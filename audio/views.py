from django.shortcuts import render
from django.http import HttpResponse
import os 
from moviepy.editor import *
from pydub import AudioSegment

# Create your views here.
def change_audio_speed2(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        speed_factor = float(request.POST['speed_factor'])

        # # Save the uploaded audio file to a temporary file
        # with open('temp_audio.mp3', 'wb+') as destination:
        #     for chunk in audio_file.chunks():
        #         destination.write(chunk)

        # Open the audio file with PyDub
        audio_segment = AudioSegment.from_file_using_temporary_files(audio_file)

        # Change the speed of the audio
        new_audio_segment = audio_segment.speedup(speed_factor)

        # Save the new audio to a file
        new_filename = 'modified_audio.mp3'
        new_audio_segment.export(new_filename, format='mp3')

        # Serve the new audio for download
        with open(new_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(new_filename))
        
        os.remove(new_filename)
            
        return response
        
    return render(request, 'audio/changespeed.html')


def change_audio_speed(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        speed_factor = float(request.POST['speed_factor'])

        # Save the uploaded audio file to a temporary file
        with open('temp_audio.mp3', 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Open the audio file with MoviePy
        audio_clip = AudioFileClip('temp_audio.mp3')

        # Change the speed of the audio
        new_audio_clip = audio_clip.fx(AudioFileClip.fx.speedx, speed_factor)

        # Save the new audio to a file
        new_filename = 'modified_audio.mp3'
        new_audio_clip.write_audiofile(new_filename)

        # Serve the new audio for download
        with open(new_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(new_filename))

        os.remove('output_audio.mp3')

        return response

    return render(request, 'audio/changespeed.html')




def change_audio_speed2(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        speed_factor = float(request.POST.get('speed_factor'))

        # Save the audio file to a temporary location
        with open('temp_audio.mp3', 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Use ffmpeg to change the speed of the audio file
        os.system(f'ffmpeg -i temp_audio.mp3 -filter:a "atempo={speed_factor}" output_audio.mp3')

        # Serve the modified audio file for download
        with open('output_audio.mp3', 'rb') as audio:
            response = HttpResponse(audio.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename=output_audio.mp3'
            return response

    return render(request, 'audio/changespeed.html')