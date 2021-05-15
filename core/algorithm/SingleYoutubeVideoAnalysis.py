import speech_recognition as sr
import moviepy.editor as mp
import pytube

Choice = input("You would like to convert a Youtube video or a Playlist(1-Single Video, 2-Playlist):" )
if Choice == '1' :
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
  # audio_output = ""
  # recognize speech using Google Speech Recognition
  result = recognizer.recognize_google(audio)

  Text_Name = Video_Name[:-4] +" Recognized Speech.txt"

  with open(Text_Name,mode ='w') as file: 
    file.write("Recognized Speech:") 
    file.write("\n") 
    file.write(result) 
    print("ready!")

elif Choice == '2':
  url = input("Enter the Youtube Playlist: ")
  p = pytube.Playlist(url)

  for i in range(0,len(p)):
      video = p.videos[i].streams.get_highest_resolution()
      video.download()
      Video_Name = video.default_filename

      clip = mp.VideoFileClip(Video_Name) 
      Audio_Name = Video_Name[:-4]+ " converted.wav"
      clip.audio.write_audiofile(Audio_Name)
      recognizer = sr.Recognizer()
      audio_file = sr.AudioFile(Audio_Name)

      with audio_file as source:
          audio = recognizer.record(source)
      # audio_output = ""
      # recognize speech using Google Speech Recognition
      result = recognizer.recognize_google(audio,langauge="ms-MY")

      Text_Name = Video_Name[:-4] +" Recognized Speech.txt"

      with open(Text_Name,mode ='w') as file: 
          file.write("Recognized Speech:") 
          file.write("\n") 
          file.write(result) 
          print("ready!")

else:
  print("Invalid input!")