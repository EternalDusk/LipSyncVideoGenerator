import os
import shutil

#careful to change these to variable addresses
data = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\data"
lexicon = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\lexicon.txt"
english = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\pretrained_models\english.zip"
output = r"C:\Users\stamp\Desktop\AutoVideoEditor\montreal-forced-aligner_win64\montreal-forced-aligner\bin\aligned"
directory = r"C:\Users\stamp\Documents\MFA\data"

#print("bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)
os.system("bin\mfa_align.exe " + data + " " + lexicon + " " + english + " " + output)

print("Deleting leftover data and cleaning up")
shutil.rmtree(directory)
print("Finished deleting data")