import os
import glob
import shutil
from shutil import copyfile
import sys
from colorama import Fore, Back, Style
import time
import VIDEO_FILES.parse as VidParser



audio_file = input("What is the audio file called? (ex: audio.wav)  ")
transcript_file = input("What is the transcript file called? (ex: transcript.txt)  ")

#==========================================================================================
#LIP SYNC ALIGNMENT
#==========================================================================================
#change these to variable addresses
data = r"data"
lexicon = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\lexicon.txt"
english = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\english.zip"
output = r"aligned"
directory = r"C:\Users\Dusk\Documents\MFA\data"

#print("bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)
os.system(r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)

print("Deleting leftover data and cleaning up")
try:
    shutil.rmtree(directory)
except Exception:
    print(FORE.blue + "\n Error hit with directory deletion, skipping \n")
    print(Style.RESET_ALL)
    pass
print("Finished")
#==========================================================================================



#==========================================================================================
#PRAAT TEXTGRID TO INFO ALIGNMENT
#==========================================================================================

print("Finding TextGrid file")
targetPattern = r"aligned\data\*.TextGrid"
TextFileFound = glob.glob(targetPattern)
fileName = os.path.basename(TextFileFound[0])
print("TextGrid file " + fileName + " found at " + TextFileFound[0])
print("Generating textgrid maker file")
newFile = fileName[:-9] + "_maker.praat"
try:
    with open(newFile, "w") as f:
        f.write("Read from file: \"" + TextFileFound[0] + "\"\n")
        f.write("selectObject: \"TextGrid " + fileName[:-9] + "\"\n")
        f.write("newList$ = List: \"no\", 3, \"yes\", \"no\"\n")
        f.write("writeFile: \"C:\\Users\\Dusk\\Desktop\\AutoVideoEditor\\aligned\\data\\info.txt\", newList$\n")
        f.close()

    print("Making info.txt")
    os.system('praat6124_win64\praat.exe --run "' + newFile + '"')
    print("info.txt file generated")
    print("cleaning generated textgrid file")
    os.remove(newFile)
except:
    print(Fore.RED + "ERROR>>info.txt or gridmaker generator failed")
    print(Style.RESET_ALL)
    sys.exit()

#==========================================================================================



#==========================================================================================
#COPYING & CLEANING UN-NEEDED FILES
#==========================================================================================

#info.txt

print("Copying info.txt")
try:
    shutil.copy(r"aligned\data\info.txt", r"VIDEO_FILES")
    print("info.txt copy successful")
except:
    print(Fore.RED + "ERROR>>unable to copy info.txt")
    print(Style.RESET_ALL)
    sys.exit()

print("Copying audio file")
try:
    audio_location = r"data\\" + audio_file
    shutil.copy(audio_location, r"VIDEO_FILES")
    print("Audio file copy successful")
except:
    print(Fore.RED + "ERROR>>audio file copy unsuccessful")
    print(Style.RESET_ALL)
    sys.exit()

try:
    print("Copying transcript file")
    transcript_location = r"data\\" + transcript_file
    shutil.copy(transcript_location, r"VIDEO_FILES")
    print("Transcript copy successful")
except:
    print(Fore.RED + "ERROR>>transcript file copy unsuccessful")
    print(Style.RESET_ALL)
    sys.exit()

#==========================================================================================



#==========================================================================================
#GENERATE LIP SYNC
#==========================================================================================
time.sleep(2)
os.chdir("VIDEO_FILES")
VidParser.parse()
#==========================================================================================



#==========================================================================================
#cleaning up loose files and moving final product
#==========================================================================================
try:
    os.remove("info.txt")
    os.remove(audio_file)
    os.remove(transcript_file)
    os.chdir("..")
    shutil.rmtree("aligned")
    os.mkdir("aligned")
    shutil.move("VIDEO_FILES//synced.mp4", os.getcwd())
except:
    print(Fore.RED + "ERROR>>loose file cleanup unsuccessful")
    print(Style.RESET_ALL)
#==========================================================================================

