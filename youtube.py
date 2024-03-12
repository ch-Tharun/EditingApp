from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from moviepy.editor import *
app = Flask(__name__)

def download_video(link,time):
    youtube_object = YouTube(link)
    clips=[]
    timestamparr=time.split(';')
    print(time)

    video_stream = youtube_object.streams.get_highest_resolution()
    
    #print(list(youtube_object.streams.filter(progressive=True).order_by('resolution').desc()))
    
    try:
        if (link.split('=')[-1] + '.mp4') not in os.listdir(os.getcwd()):
            video_stream.download(output_path=os.getcwd(),filename=link.split('=')[-1] + '.mp4')
        clip=VideoFileClip(filename=link.split('=')[-1] + '.mp4')
        for timestamp in range(len(timestamparr)):
            starttimestamp,endtimestamp= timestamparr[timestamp].split("-")
            print(timestamparr)
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
        clip.write_videofile("clip.mp4")
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
    print(link)
    success = download_video(link,time)
    if success:
        filename = link.split('=')[-1] + '.mp4'  # Extract video ID from URL
        file_path = os.path.join(os.getcwd(), "clip.mp4")
        print(file_path)
        return send_file(file_path, as_attachment=True)
    else:
        return "Download failed"

if __name__ == '__main__':
    app.run(debug=True)