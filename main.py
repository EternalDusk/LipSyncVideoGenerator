import os
import os.path
import glob
import shutil
import sys
import time
import math
import re

from PIL import Image, ImageDraw, ImageFont
from colorama import Fore, Back, Style, init

#Override ANSI code errors
init(strip=False, autoreset=True)

#===TODO===
# 1) add function to check for correct usage (correct number of arguments, etc.)
# 2) add check for all character files
# 3) add check for all pose/tagged files
# 4) Update mouth numbering and pictures
#==========

#===CONSTANT FILE PATHS/VARIABLES===
data = r"data"
lexicon = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\lexicon.txt"
english = r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\english.zip"
output = r"aligned"
directory = os.path.join(r'C:\Users', os.getlogin(), 'Documents', 'MFA', 'data')

headers = 'Min Time', 'Tier', 'Text', 'Max Time'  # Column names
#=========================


#===FILE CHECKING/LOADING===
audio_file = sys.argv[1]
transcript_file = sys.argv[2]

if audio_file.endswith(".wav") or audio_file.endswith(".mp3"):
    #load audio file
    if os.path.isfile("data/" + audio_file) != True:
        raise Exception(Fore.RED + "Given audio file not found!")
else:
    raise Exception(Fore.RED + "Incorrect audio filetype, must be .wav or .mp3")

if transcript_file.endswith(".txt"):
    #load audio file
    if os.path.isfile("data/" + transcript_file) != True:
        raise Exception(Fore.RED + "Given transcript file not found!")
else:
    raise Exception(Fore.RED + "Incorrect transcript filetype, must be .txt")
#===========================

#RUN ALIGNMENT PROGRAM
os.system(r"montreal-forced-aligner_win64\montreal-forced-aligner\bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)


#===TEXTGRID GENERATION===

#finding textgrid file (need a better way of doing the file search)
targetPattern = r"aligned\data\*.TextGrid"
TextFileFound = glob.glob(targetPattern)
fileName = os.path.basename(TextFileFound[0])

newFile = fileName[:-9] + "_maker.praat"
try:
    with open(newFile, "w") as f:
        f.write("Read from file: \"" + TextFileFound[0] + "\"\n")
        f.write("selectObject: \"TextGrid " + fileName[:-9] + "\"\n")
        f.write("newList$ = List: \"no\", 3, \"yes\", \"no\"\n")
        f.write("writeFile: \"" + os.getcwd() + "\\aligned\\data\\info.txt\", newList$\n")
        f.close()

    os.system('praat6124_win64\praat.exe --run "' + newFile + '"')

except:
    raise Exception(Fore.RED + "ERROR: info.txt or gridmaker generator failed")
    sys.exit()
#=========================


#table array creation
pose_table = []
transcript_pose_table = []

#===CONSTRUCT TABLES===
#open file as table
with open(r"aligned\data\info.txt") as file:
    datatable = [line.split() for line in file.read().splitlines()]

#get longest value for each column (for best table viewing)
widths = [max(len(value) for value in col)
            for col in zip(*(datatable + [headers]))]

#sort table
i = 0
while i < len(datatable):
    if "words" in datatable[i]:
        if datatable[i][2] == '<unk>':
            pose_table.append(datatable[i])
            datatable.pop(i)
        else:
            datatable.pop(i)
    elif "tier" in datatable[i]:
        datatable.pop(i)

    i += 1

#format and print table of data
format_spec = '{:{widths[0]}}  {:>{widths[1]}}  {:>{widths[2]}}  {:>{widths[3]}}'

print(format_spec.format(*headers, widths=widths))
for fields in datatable:
    print(format_spec.format(*fields, widths=widths))
#======================



#===FILL POSE TABLE===
with open("data\\" + transcript_file) as infile:
    for line in infile:
        #find markers <> to define pose
        transcript_pose_table.append(re.search('\<(.*)\>', line).group(1))

p = 0
while p < len(transcript_pose_table):
    pose_table[p][2] = transcript_pose_table[p]
    p += 1

print("\n")
for fields2 in pose_table:
    print(format_spec.format(*fields2, widths=widths))
#==================================

#==POSE AND PHONEME TABLE FILLING==
i = 0
j = 0
u = 0
pose_table.insert(0, [pose_table[u][0], pose_table[u][1], pose_table[u][2], pose_table[u][3]])

phoneme_frames = []

while i < len(datatable):
    start = datatable[i][0]
    end = datatable[i][-1]
    keyframe = float(start)
    while (keyframe < float(end)):
        split = (keyframe - float(end))
        if (split <= -0.001):
            if (u < (int(len(pose_table)) - 1)):
                if (float(keyframe) >= float(pose_table[u+1][0])):
                    u += 1
            else:
                u += 0
            phoneme_frames.append([j, datatable[i][2], pose_table[u][2]])
            keyframe += (1/100)
            j += 1
        else:
            keyframe += (1)
    i += 1
#==================================

#===FRAME CREATION===
k = 0
print(Fore.BLUE + "Starting image output")
for i in range(len(phoneme_frames)):
    try:
        #WRITING IMAGE
        img = Image.new('RGBA', (1280, 720), color = (255, 255, 255, 0))
        d = ImageDraw.Draw(img)


        #mouth selection
        if (phoneme_frames[k][1]) in ['sil', 'sp', 'M', 'N', 'NG', 'P']:
            mouth_path = ".\\" + character_name + "\\mouths\\1.png"
        if (phoneme_frames[k][1]) in ['AA0', 'AA1', 'AA2', 'AO0', 'AO1', 'AO2']:
            mouth_path = ".\\" + character_name + "\\mouths\\2.png"
        if (phoneme_frames[k][1]) in ['R', 'AW0', 'AW1', 'AW2', 'UW0', 'UW1', 'UW2', 'W', 'AY0', 'AY1', 'AY2', 'ER0', 'ER1', 'ER2', 'AE0', 'AE1', 'AE2', 'EY0', 'EY1', 'EY2', 'S', 'UH0', 'UH1', 'UH2', 'OY0', 'OY1', 'OY2', 'OW0', 'OW1', 'OW2', 'EH']:
            mouth_path = ".\\" + character_name + "\\mouths\\3.png"
        if (phoneme_frames[k][1]) in ['AH0', 'AH1', 'AH2']:
            mouth_path = ".\\" + character_name + "\\mouths\\4.png"
        if (phoneme_frames[k][1]) in ['B']:
            mouth_path = ".\\" + character_name + "\\mouths\\7.png"
        if (phoneme_frames[k][1]) in ['CH', 'SH', 'ZH']:
            mouth_path = ".\\" + character_name + "\\mouths\\8.png"
        if (phoneme_frames[k][1]) in ['DH']:
            mouth_path = ".\\" + character_name + "\\mouths\\11.png"
        if (phoneme_frames[k][1]) in ['F', 'V']:
            mouth_path = ".\\" + character_name + "\\mouths\\12.png"
        if (phoneme_frames[k][1]) in ['H', 'HH']:
            mouth_path = ".\\" + character_name + "\\mouths\\13.png"
        if (phoneme_frames[k][1]) in ['JH']:
            mouth_path = ".\\" + character_name + "\\mouths\\14.png"
        if (phoneme_frames[k][1]) in ['K', 'G', 'D', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'S']:
            mouth_path = ".\\" + character_name + "\\mouths\\15.png"
        if (phoneme_frames[k][1]) in ['T', 'Y', 'Z']:
            mouth_path = ".\\" + character_name + "\\mouths\\18.png"
        if (phoneme_frames[k][1]) in ['TH', 'L']:
            mouth_path = ".\\" + character_name + "\\mouths\\19.png"


        mouth = Image.open(mouth_path, 'r')
        current_anim_pose = (".\\" + character_name + "\\" + (phoneme_frames[k][2])[1:] + ".png")
        pose = Image.open(current_anim_pose, 'r')

        #mouth placement
        img.paste(pose, (220, 220), mask=pose)
        if ((phoneme_frames[k][2])[1:] == "idle"):
            img.paste(mouth, (470,400), mask=mouth)
        if ((phoneme_frames[k][2])[1:] == "proud"):
            img.paste(mouth, (470,405), mask=mouth)
        if ((phoneme_frames[k][2])[1:] == "wave"):
            img.paste(mouth, (465,400), mask=mouth)


        img.save('frame_' + str(k) + '.png')
        k += 1

    except Exception as e:
        print("List Ended with error " + str(e))
        k = len(phoneme_frames) + 10

print(Style.RESET_ALL)
#====================

#BUILD VIDEO
os.system('ffmpeg -y -r 100 -f image2 -s 600x900 -i "frame_%d.png" -i .\\data\\' + audio_file + ' -pix_fmt yuv420p draft.mp4')
os.system('ffmpeg -y -i draft.mp4 -r 30 synced.mp4')

#===CLEANUP===
if os.path.exists(directory):
    shutil.rmtree(directory)
if os.path.exists(newFile):
    os.remove(newFile)

filelist = [ f for f in os.listdir(os.getcwd()) if f.endswith(".png") ]
for f in filelist:
    os.remove(os.path.join(os.getcwd(), f))
os.remove(r'draft.mp4')
shutil.rmtree("aligned")
#=============
