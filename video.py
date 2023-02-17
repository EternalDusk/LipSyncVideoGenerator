import os
import glob
import shutil
from shutil import copyfile


#==========================================================================================
#LIP SYNC ALIGNMENT
#==========================================================================================
#careful to change these to variable addresses
data = r"C:\Users\stamp\Desktop\AutoVideoEditor\data"
lexicon = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\lexicon.txt"
english = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\english.zip"
output = r"C:\Users\stamp\Desktop\AutoVideoEditor\aligned"
directory = r"C:\Users\stamp\Documents\MFA\data"

#print("bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)
os.system(r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)

print("Deleting leftover data and cleaning up")
try:
    shutil.rmtree(directory)
except Exception:
    print("\n Error hit with directory deletion, skipping \n")
    pass
print("Finished")
#==========================================================================================



#==========================================================================================
#PRAAT TEXTGRID TO INFO ALIGNMENT
#==========================================================================================

print("Finding TextGrid file")
targetPattern = r"C:\Users\stamp\Desktop\AutoVideoEditor\aligned\data\*.TextGrid"
glob.glob(targetPattern)
print("TextGrid file found")
print("Generating info.txt file")
os.system('praat6124_win64\praat.exe --run "grid_maker.praat"')
print("info.txt file generated")

#==========================================================================================



#==========================================================================================
#COPYING & CLEANING UN-NEEDED FILES
#==========================================================================================

#info.txt

#print("Copying info.txt")
#shutil.copy(r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\data\info.txt", r"C:\Users\stamp\Desktop\AutoVideoEditor\VIDEO FILES")
#print("info.txt copy successful")

#print("Copying audio file")
#shutil.copy(r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\data\thing.wav", r"C:\Users\stamp\Desktop\AutoVideoEditor\VIDEO FILES")
#print("Audio file copy successful")

#print("Copying transcript file")
#shutil.copy(r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\data\thing.txt", r"C:\Users\stamp\Desktop\AutoVideoEditor\VIDEO FILES")
#print("Transcript copy successful")

#==========================================================================================



#fix with actual character
#==========================================================================================
#GENERATE LIP SYNC
#==========================================================================================

#==========================================================================================
