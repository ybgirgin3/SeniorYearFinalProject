from imutils import contours
from skimage import measure
from numpy import interp
import numpy as np
#import pigpio
import time
import cv2
# import servos

# open camera for capturing frames
# wsl cant open camera 
#cap = cv2.VideoCapture(0)

# this just for in ubuntu 
cap = cv2.VideoCapture('digital/vid1.mp4')



# servo pinleri
panServo = 4
tiltServo = 17

# en baştaki pozisyon
panPos = 1500
tiltPos = 1500

"""
servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, panPos)
servo.set_servo_pulsewidth(tiltServo, tiltPos)
"""

minMov = 1
maxMov = 10



def func(x, y, w, h):
    global panPos
    global tiltPos

    # draw circle around the flame
    # cv2.circle(frame, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    # put text on the circle
    # cv2.putText(frame, "#{}".format(i+1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # we gonna calculate the distance pan tilt servos will go for.
    # Flame far away from centre means servos will cover more distance
    # and flame near the centre means servos will go for less distance
    
    # If the pan and tilt servos position will be in 0 to 180 degrees (500=0 degree and 2500=180 degree)
    # Servos will move to that position otherwise these will stay in the current position
    
    # int(x+(w/2)) > 360 means flame is on the right side of the frame
    if int(x+(w/2)) > 360:
            panPos = int(panPos - interp(int(x+(w/2)), (360, 640), (minMov, maxMov)))

    # int(x+(w/2)) < 280 means flame is on the left side of the frame
    elif int(x+(w/2)) < 280:
            panPos = int(panPos + interp(int(x+(w/2)), (280, 0), (minMov, maxMov)))

    
    if int(y+(h/2)) > 280:
            tiltPos = int(tiltPos + interp(int(y+(h/2)), (280, 480), (minMov, maxMov)))

    elif int(y+(h/2)) < 200:
            tiltPos = int(tiltPos - interp(int(y+(h/2)), (200, 0), (minMov, maxMov)))

 	
    if not panPos > 2500 or not panPos < 550:
        #servo.set_servo_pulsewidth(panServo, panPos)
        print('panServo: {}'.format(panPos))

    
    if not tiltPos > 2500 or tiltPos < 550:
        #servo.set_servo_pulsewidth(tiltServo, tiltPos)
        print('tiltServo: {}'.format(tiltPos))

   



while True:
    # Videodan veri oku
    ret, frame = cap.read()
    #frame = cv2.flip(frame, -1)

    # düzgün çalışmıyor
    #face_cascade = cv2.CascadeClassifier('xml/lbpcascade_frontalface_improved.xml')

    face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # print(len(faces))
    # Display the resulting frame
    for (x,y,w,h) in faces:
         func(x, y, w, h)
    # print('width, height: {}, {} '.format(width,height))
    # değerleri geri dön ya da direk olarak fonksiyon içinde kullan
    # return width, height
        # servos.Servos(width, height, int(cX), int(cY))

    # Display the resulting frame
    #cv2.flip(frame, -1)
    cv2.imshow('frame', frame)
    # cv2.imshow('frame', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
