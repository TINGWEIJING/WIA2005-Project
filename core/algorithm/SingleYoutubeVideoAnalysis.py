import speech_recognition as sr
import moviepy.editor as mp
import pytube
import os 

url = input("Enter the Youtube-url: ")
#Video_Name = input("Enter the Video Name")
youtube = pytube.YouTube(url)
video = youtube.streams.get_highest_resolution()
video.download()
Video_Name=video.default_filename
print(Video_Name, "Downloaded!")


clip = mp.VideoFileClip(Video_Name) 
Audio_Name = Video_Name[:-4]+ " converted.wav"
clip.audio.write_audiofile(Audio_Name)
recognizer = sr.Recognizer()
audio_file = sr.AudioFile(Audio_Name)

with audio_file as source:
  audio = recognizer.record(source)
  print("done!")
# audio_output = ""
# recognize speech using Google Speech Recognition
result = recognizer.recognize_google(audio)
print(result)

Text_Name = Video_Name +"Recognized Speech.txt"
with open(Text_Name,mode ='w') as file: 
   file.write("Recognized Speech:") 
   file.write("\n") 
   file.write(result) 
   print("ready!")

