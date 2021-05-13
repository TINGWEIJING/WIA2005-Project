import speech_recognition as sr
import moviepy.editor as mp
import pytube

url = input("Enter the Youtube Playlist: ")
#Video_Name = input("Enter the Video Name")
p = pytube.Playlist(url)

for i in range(0,len(p)):
    print(i)
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
    result = recognizer.recognize_google(audio)

    Text_Name = Video_Name[:-4] +"Recognized Speech.txt"

    with open(Text_Name,mode ='w') as file: 
        file.write("Recognized Speech:") 
        file.write("\n") 
        file.write(result) 
        print("ready!")

