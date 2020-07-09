import easygui
import sys
import re
from pathlib import Path
import subprocess
import os 

os.chdir('/home/parth/Music')
file_path = Path(easygui.fileopenbox())
parent_path = file_path.parent
# print("type(parent_path) = ",type(parent_path))
trimmed_file_path = parent_path/(file_path.stem + '_trimmed' + file_path.suffix)
print(file_path,trimmed_file_path)

override = True

if trimmed_file_path.exists() :
    msg = (str(trimmed_file_path) + " already exists , Press Yes to replace the file , No to abort the trimming")
    choices = ['Yes','No']
    choice = easygui.buttonbox(msg,choices = choices)
    print(choice)
    override = choice == 'Yes'

print(override)

title = "Audio Trimmer "
msg = "Enter time information for trimming "
field_names = ["Start time(in seconds) " , "End time (in seconds) "]
field_values = easygui.multenterbox(msg,title,field_names)


start_time = field_values[0]
end_time = field_values[1]
print("start time = ",start_time)
print("end time = ",end_time)

r = re.compile(r'[\D]')

try : 
    if r.search(start_time+end_time) :
        raise ValueError("both start time and end time should be numerical value")
    else :
        start_time=int(start_time)
        end_time = int(end_time)
    if start_time > end_time :
        raise ValueError("start time cannot be greater than end time")
except ValueError as e:
    print("An exception flew by")
    easygui.msgbox(getattr(e,'message',e),'Error !!')
    raise    

args = ['ffmpeg']

if override :
    args += ['-y']
else :
    args+=['-n']

args += ['-i',file_path,'-ss',str(start_time),'-to',str(end_time),'-c','copy',trimmed_file_path]

print(args)

try :
    res = subprocess.run(args,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
except subprocess.CalledProcessError as e :
    easygui.msgbox("Unable to trim file , operation failed . Check the parameters and try again",'Task failed !')
    raise
# print(res)
easygui.msgbox("File trimmed saved successfully , trimmed file location = " + str(trimmed_file_path),'Success !')
