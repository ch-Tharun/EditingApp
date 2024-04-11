from flask import Flask, render_template, request, send_file
import moviepy.audio
import moviepy.audio.fx
import moviepy.audio.fx.all
import moviepy.audio.fx.volumex
from pytube import YouTube
import os
import moviepy
from moviepy.editor import *
from pytube.cli import on_progress
app = Flask(__name__)

def download_video(link,time,file,selectFloat):
    youtube_object = YouTube(link,on_progress_callback=on_progress)
    clips=[]
    timestamparr=time.split(';')
    print(time)
    print(file)
    filepath=os.path.join(r"C:\Users\Tharun\Downloads",file)
    print(filepath)

    video_stream = youtube_object.streams.get_highest_resolution()
    
    #print(list(youtube_object.streams.filter(progressive=True).order_by('resolution').desc()))
    
    try:
        if (link.split('=')[-1] + '.mp4') not in os.listdir(os.getcwd()):
            video_stream.download(output_path=os.getcwd(),filename=link.split('=')[-1] + '.mp4')
        clip=VideoFileClip(filename=link.split('=')[-1] + '.mp4')
        
        
        
        #audio_clip=clip.audio
        #audio_clip.write_audiofile("audio.mp3")
        for timestamp in range(len(timestamparr)):
            starttimestamp,endtimestamp= timestamparr[timestamp].split("-")
            #print(timestamparr)
            sth,stm,sts=starttimestamp.strip().split(':')
            eth,etm,ets=endtimestamp.strip().split(':')
            if(eth.strip() != '00' and etm.strip() != '00' and ets.strip() != '00'):
                clips.append(clip.subclip((int(sth.strip())*60*60) + (int(stm.strip())*60) + (int(sts.strip())),(int(eth.strip())*60*60) + (int(etm.strip())*60) + (int(ets.strip()))))
            else:  
                clips.append(clip.subclip((int(sth.strip())*60*60) + (int(stm.strip())*60) + (int(sts.strip())),(int(eth.strip())*60*60) + (int(etm.strip())*60) + (int(ets.strip()))))

        #clip1=clip.subclip(0,10)
        #clip2=clip.subclip(10,20)
        #clip3=clip.subclip(50,59)
        clip=concatenate_videoclips(clips)
        print(clip.duration)
        
        audiofile=AudioFileClip(filename=filepath)
        #audio_back=AudioFileClip("clipped.mp3")
        audiofile=audiofile.subclip(0,clip.duration)
        print(float(selectFloat))
        newclip=moviepy.audio.fx.all.volumex(audiofile,float(selectFloat))
        newclip.write_audiofile("clipped.mp3")

        final_audio = CompositeAudioClip([clip.audio, AudioFileClip('clipped.mp3')])
        final_clip = clip.set_audio(final_audio)
        final_clip.write_videofile("clip.mp4")
        #comp=VideoFileClip("clip.mp4")
        #final_audio=CompositeAudioClip([comp.audio,audio_back])
        #comp.set_audio(final_audio).write_videofile("composed.mp4")
        return True
    except Exception as e:
        print("An error has occurred:", e)
        return False

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    link = data.get('link')
    time=data.get('time')
    file=data.get('file')
    selectFloat=data.get('selectFloat')
    print(link)
    success = download_video(link,time,file,selectFloat)
    if success:
        filename = link.split('=')[-1] + '.mp4'  # Extract video ID from URL
        file_path = os.path.join(os.getcwd(), "clip.mp4")
        print(file_path)
        return send_file(file_path, as_attachment=True)
    else:
        return "Download failed"

if __name__ == '__main__':
    app.run(debug=True)