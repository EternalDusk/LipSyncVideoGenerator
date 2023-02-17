from PIL import Image, ImageDraw, ImageFont
import os
import os.path
import math
import time
import re

data_filename = 'info.txt'
headers = 'Min Time', 'Tier', 'Text', 'Max Time'  # Column names.

pose_table = []
transcript_pose_table = []

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



with open('thing.txt') as infile:
    for line in infile:
        transcript_pose_table.append(re.search('\<(.*)\>', line).group(1))

p = 0
while p < len(transcript_pose_table):
    pose_table[p][2] = transcript_pose_table[p]
    p += 1



print("\n")
for fields2 in pose_table:
    print(format_spec.format(*fields2, widths=widths))

i = 0
j = 0
u = 0



u = 0
pose_table.insert(0, [pose_table[u][0], pose_table[u][1], pose_table[u][2], pose_table[u][3]])

fix = 1

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


k = 0





while k <= len(phoneme_frames):
    try:
        print(phoneme_frames[k])
        
        
        #WRITING IMAGE
        img = Image.new('RGBA', (1280, 720), color = (54, 52, 49, 0))
        d = ImageDraw.Draw(img)
        
        tv_large = Image.open("Character Images\crt-tv.png")
        tv = tv_large.resize((714, 728))
        
        scp079_small = Image.open("Character Images\scp079.jpg")
        scp079 = scp079_small.resize((680, 680))
        
        
        if (phoneme_frames[k][1] == "sil"):
            img.paste(tv, (20, 20), mask=tv)
        elif (phoneme_frames[k][1] == "sp"):
            img.paste(tv, (20, 20), mask=tv)
        elif (phoneme_frames[k][1] == "spn"):
            img.paste(tv, (20, 20), mask=tv)
        else:
            img.paste(scp079, (20, 20))
            img.paste(tv, (20, 20), mask=tv)
        

        img.save('frame_' + str(k) + '.png')
        k += 1
    except Exception as e:
        print("List Ended with error " + str(e))
        k = len(phoneme_frames) + 10

os.system('ffmpeg -r 100 -f image2 -s 600x900 -i "frame_%d.png" -i thing.wav -pix_fmt yuv420p test.mp4')

filelist = [ f for f in os.listdir(r'C:\Users\stamp\Desktop\AutoVideoEditor\VIDEO FILES') if f.endswith(".png") ]
for f in filelist:
    os.remove(os.path.join(r'C:\Users\stamp\Desktop\AutoVideoEditor\VIDEO FILES', f))
os.system('ffmpeg -i test.mp4 -r 30 synced.mp4')
os.remove(r'test.mp4')