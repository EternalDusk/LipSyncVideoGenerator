import os
import glob
import shutil
from shutil import copyfile
import sys
from colorama import Fore, Back, Style, init
import time
import VIDEO_FILES.parse as VidParser

#override ANSI codes
init(strip=False, autoreset=True)


#==AUDIO FILE HANDLING==
#bool loop
audio_given = False

while(audio_given == False):
    audio_file = input("What is the audio file called? (ex: audio, test.wav)  ")
    audio_extension = audio_file[-4:]

    if (audio_extension != ".wav"):
        if ("." in audio_file):
            print(Fore.RED + "ERROR: The audio file must be a .wav file")
        else:
            if (os.path.exists("data/" + audio_file + ".wav") == False):
                print(Fore.RED + "ERROR: Audio file " + audio_file + ".wav does not exist")
            else:
                audio_file += ".wav"
                audio_given = True
    elif (os.path.exists("data/" + audio_file) == False):
        print(Fore.RED + "ERROR: Audio file " + audio_file + " does not exist")
    else:
        audio_given = True
#=======================


#==TRANSCRIPT FILE HANDLING==
#bool loop
transcript_given = False

while(transcript_given == False):
    transcript_file = input("What is the transcript file called? (ex: transcript.txt)  ")
    transcript_extension = transcript_file[-4:]

    if (transcript_extension != ".txt"):
        if ("." in transcript_file):
            print(Fore.RED + "ERROR: The transcript file must be a .txt file")
        else:
            if (os.path.exists("data/" + transcript_file + ".txt") == False):
                print(Fore.RED + "ERROR: Transcript file " + transcript_file + ".txt does not exist")
            else:
                transcript_file += ".txt"
                transcript_given = True
    elif (os.path.exists("data/" + transcript_file) == False):
        print(Fore.RED + "ERROR: Transcript file " + transcript_file + " does not exist")
    else:
        transcript_given = True
#============================



#==DATA LOCATIONS==
data = r"data"
lexicon = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\lexicon.txt"
english = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\english.zip"
output = r"aligned"
directory = os.path.join(r'C:\Users', os.getlogin(), 'Documents', 'MFA', 'data')
#==================


#==ALIGNMENT==
os.system(r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)
#=============


#==CLEANUP==
print("Deleting leftover data and cleaning up")
try:
    shutil.rmtree(directory)
except Exception:
    print(FORE.blue + "\n ALERT: Directory deletion failed, skipping \n")
    pass
print("Finished")
#===========


#==PRAAT TEXTGRID TO INFO ALIGNMENT==

print("Finding TextGrid file")
targetPattern = r"aligned\data\*.TextGrid"
TextFileFound = glob.glob(targetPattern)
fileName = os.path.basename(TextFileFound[0])
print("TextGrid file " + fileName + " found at " + TextFileFound[0])


print("Generating textgrid maker file")
#generate new file maker
newFile = fileName[:-9] + "_maker.praat"
try:
    with open(newFile, "w") as f:
        f.write("Read from file: \"" + TextFileFound[0] + "\"\n")
        f.write("selectObject: \"TextGrid " + fileName[:-9] + "\"\n")
        f.write("newList$ = List: \"no\", 3, \"yes\", \"no\"\n")
        f.write("writeFile: \"" + os.getcwd() + "\\aligned\\data\\info.txt\", newList$\n")
        f.close()

    print("Making info.txt")
    os.system('praat6124_win64\praat.exe --run "' + newFile + '"')
    print("info.txt file generated")
    print("cleaning generated textgrid file")
    os.remove(newFile)
except:
    print(Fore.RED + "ERROR: info.txt or gridmaker generator failed")
    sys.exit()

#====================================



#==COPYING FILES AND CLEANING UP==

#info.txt
print("Copying info.txt")
try:
    shutil.copy(r"aligned\data\info.txt", r"VIDEO_FILES")
    print("info.txt copy successful")
except:
    print(Fore.RED + "ERROR: Unable to copy info.txt")
    sys.exit()


#audio file
print("Copying audio file")
try:
    audio_location = r"data\\" + audio_file
    shutil.copy(audio_location, r"VIDEO_FILES")
    print("Audio file copy successful")
except:
    print(Fore.RED + "ERROR: Unable to copy audio file")
    sys.exit()


#transcript file
try:
    print("Copying transcript file")
    transcript_location = r"data\\" + transcript_file
    shutil.copy(transcript_location, r"VIDEO_FILES")
    print("Transcript copy successful")
except:
    print(Fore.RED + "ERROR: Unable to copy transript file")
    sys.exit()

#=================================



#==GENERATE LIP SYNC==
#allowing 2 seconds for copy jobs to finish
time.sleep(2)
os.chdir("VIDEO_FILES")
VidParser.parse()
#=====================



#==MORE CLEAN UP AND MOVING FINAL PRODUCT==
try:
    os.remove("info.txt")
    os.remove(audio_file)
    os.remove(transcript_file)
    os.chdir("..")
    shutil.rmtree("aligned")
    shutil.move("VIDEO_FILES//synced.mp4", os.getcwd())
except Exception as e:
    print(Fore.RED + "ERROR: Loose file cleanup unsuccessful" + str(e))
#==========================================
