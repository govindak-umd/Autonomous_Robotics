import numpy as np
import cv2
import time
import datetime
import os
import glob

# create a unique folder to store images in
today = time.strftime("%Y%m%d-%H%M%S")
print(today)
os.system("sudo mkdir " + today)

# define the codec and create VideoWriter object
fps_out = 10
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(today + ".avi", fourcc, fps_out, (1280, 720))

# reocrd n-images into the current directory
for i in range (0,10):
    image = "sudo raspistill -w 1280 -h 720 -hf -vf -o /home/pi/All_Py_Files/" + today + "/" + str(i) + ".jpg"
    os.system(image)
    print("Saved image: ", i)
    time.sleep(0.1)

# find all images recorded during the run
files = glob.glob(today + "/*.jpg")
print(files)
files = sorted(glob.glob(today + "/*.jpg"))
print(files)

# loop through and print frames to video file
for x in files:
    print(x)
    image_out = cv2.imread(x)
    out.write(image_out)

print("Video: " + today + ".avi is now ready for viewing!")
