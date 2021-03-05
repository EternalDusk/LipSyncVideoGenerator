from PIL import Image, ImageDraw, ImageFont
import os
import os.path
import math
import time
import re
from progressbar import progressbar
from colorama import init, Fore, Back, Style

init(autoreset=True)
def parse():

    data_filename = 'info.txt'

    headers = 'Min Time', 'Tier', 'Text', 'Max Time'  # Column names.

    pose_table = []
    transcript_pose_table = []


    #==CONVERT DATA INTO VIEWABLE TABLESET==
    # Read the data from file into a list-of-lists table.
    with open(data_filename) as file:
        datatable = [line.split() for line in file.read().splitlines()]
    # Find the longest data value or header to be printed in each column.
    widths = [max(len(value) for value in col)
                for col in zip(*(datatable + [headers]))]
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
    print("\n")
    # Print heading followed by the data in datatable.
    # (Uses '>' to right-justify the data in some columns.)
    format_spec = '{:{widths[0]}}  {:>{widths[1]}}  {:>{widths[2]}}  {:>{widths[3]}}'
    print(format_spec.format(*headers, widths=widths))
    for fields in datatable:
        print(format_spec.format(*fields, widths=widths))
    #=======================================



    #==POSE TABLE CREATION==
    with open('transcript.txt') as infile:
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
    #======================


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



    #==FRAME CREATION==
    k = 0
    print(Fore.BLUE + "Starting image output")
    for i in range(len(phoneme_frames)):
        try:
            #print(phoneme_frames[k])


            #WRITING IMAGE
            img = Image.new('RGBA', (1280, 720), color = (255, 255, 255, 0))
            d = ImageDraw.Draw(img)


            #mouth selection
            if (phoneme_frames[k][1]) in ['sil', 'sp', 'M', 'N', 'NG', 'P']:
                pose_path = ".\\chibidusk\\mouths\\1.png"
            if (phoneme_frames[k][1]) in ['AA0', 'AA1', 'AA2', 'AO0', 'AO1', 'AO2']:
                pose_path = ".\\chibidusk\\mouths\\2.png"
            if (phoneme_frames[k][1]) in ['R', 'AW0', 'AW1', 'AW2', 'UW0', 'UW1', 'UW2', 'W', 'AY0', 'AY1', 'AY2', 'ER0', 'ER1', 'ER2', 'AE0', 'AE1', 'AE2', 'EY0', 'EY1', 'EY2', 'S', 'UH0', 'UH1', 'UH2', 'OY0', 'OY1', 'OY2', 'OW0', 'OW1', 'OW2', 'EH']:
                pose_path = ".\\chibidusk\\mouths\\3.png"
            if (phoneme_frames[k][1]) in ['AH0', 'AH1', 'AH2']:
                pose_path = ".\\chibidusk\\mouths\\4.png"
            if (phoneme_frames[k][1]) in ['B']:
                pose_path = ".\\chibidusk\\mouths\\7.png"
            if (phoneme_frames[k][1]) in ['CH', 'SH', 'ZH']:
                pose_path = ".\\chibidusk\\mouths\\8.png"
            if (phoneme_frames[k][1]) in ['DH']:
                pose_path = ".\\chibidusk\\mouths\\11.png"
            if (phoneme_frames[k][1]) in ['F', 'V']:
                pose_path = ".\\chibidusk\\mouths\\12.png"
            if (phoneme_frames[k][1]) in ['H', 'HH']:
                pose_path = ".\\chibidusk\\mouths\\13.png"
            if (phoneme_frames[k][1]) in ['JH']:
                pose_path = ".\\chibidusk\\mouths\\14.png"
            if (phoneme_frames[k][1]) in ['K', 'G', 'D', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'S']:
                pose_path = ".\\chibidusk\\mouths\\15.png"
            if (phoneme_frames[k][1]) in ['T', 'Y', 'Z']:
                pose_path = ".\\chibidusk\\mouths\\18.png"
            if (phoneme_frames[k][1]) in ['TH', 'L']:
                pose_path = ".\\chibidusk\\mouths\\19.png"


            mouth = Image.open(pose_path, 'r')
            current_anim_pose = (".\\chibidusk\\" + (phoneme_frames[k][2])[1:] + ".png")
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
    #==================


    #==VIDEO BUILDING==
    os.system('ffmpeg -y -r 100 -f image2 -s 600x900 -i "frame_%d.png" -i transcript.wav -pix_fmt yuv420p test.mp4')
    #==================



    #==FILE CLEANUP==
    filelist = [ f for f in os.listdir(os.getcwd()) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(os.getcwd(), f))
    os.system('ffmpeg -y -i test.mp4 -r 30 synced.mp4')
    os.remove(r'test.mp4')
    #================
