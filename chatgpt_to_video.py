import json
import pyttsx3
from pyChatGPT import ChatGPT
import selenium_firefox
import os
from mutagen.mp3 import MP3
from PIL import Image
from pathlib import Path
from moviepy import editor

#uses pyChatGPT module to retrieve a ChatGPT response string
session_token = "[get from ChatGPT session token element]"
video_name = "[name of video]"
prompt = "[prompt for ChatGPT to respond to]"
api = ChatGPT(session_token,
              conversation_id="[conversation id for ChatGPT element]",
              auth_type="[service used to authenticate]", #google, openai
              email="[login email]",
              password="[login password]",
              moderation=False,
              window_size=(1024, 768),
              verbose=True)
resp = api.send_message(prompt) #pulls data from response into a dictionary
api.reset_conversation()
api.clear_conversations()
api.refresh_chat_page()
response_string = resp["message"] #pulls response string from resp dictionary
print(response_string)

#converts chatGPT response string with pyttsx3 module to text-to-speech as an mp3 file
engine = pyttsx3.init()
engine.save_to_file(response_string, f"{video_name}.mp3")
engine.runAndWait()

# #class for converting mp3 to mp4
class MP3ToMP4:
    def __init__(self, folder_path, audio_path, video_path_name):
        self.folder_path = folder_path
        self.audio_path = audio_path
        self.video_path_name = video_path_name
        self.create_video()
        
    #get's the length of mp3
    def get_length(self):
        song = MP3(self.audio_path)
        print("mp3 length has been determined")
        return int(song.info.length)
    
    #makes a list of the png's in the image folder
    def get_images(self):
        path_images = Path(self.folder_path)
        images = list(path_images.glob("*.png"))
        image_list = list()
        for image_name in images:
            image = Image.open(image_name).resize((800, 800), Image.ANTIALIAS)
            image_list.append(image)
        print("images have been located")
        return image_list
    
    #creates gif to combine with audio
    def create_video(self):
        length_audio = self.get_length()
        image_list = self.get_images()
        duration = int(length_audio / len(image_list)) * 1000
        image_list[0].save(self.folder_path + "temp.gif",
                           save_all=True,
                           append_images=image_list[1:],
                           duration=duration)
        self.combine_audio()
        print("video has been created")
        
    #combines audio with the gif and saves as an mp4 file
    def combine_audio(self):
        video = editor.VideoFileClip(self.folder_path + "temp.gif")
        audio = editor.AudioFileClip(self.audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile(self.video_path_name, fps=60, codec="libx264")
        print("video has been combined with audio")

folder_path = r"[base path for temp files]"
audio_path = r"[path for mp3]"
video_path_name = r"[path for mp4]" + f"\{video_name}.mp4" 
MP3ToMP4(folder_path, audio_path, video_path_name)

