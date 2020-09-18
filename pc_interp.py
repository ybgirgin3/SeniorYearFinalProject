#
# this is the pc version of the servo controlling
#
from imutils import contours
from skimage import measure
from numpy import interp
import numpy as np
#import pigpio
import time
import cv2
# import servos

# open camera for capturing frames
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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
    cv2.circle(frame, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
    # put text on the circle
    cv2.putText(frame, "#{}".format(i+1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

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

    # no need to flip camera while on pc
    #frame = cv2.flip(frame, -1)
    
    ## get resolution of frame
    # TODO:
    # return width and height of frame
    # return x and y axis of detected flame and found measure of flame to the frame center 
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # print('width, height: {}, {}'.format(width, height))
    

    # okunan her bir karenin üzerinde işlem yap
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # flame rgb codes: 266, 88, 34
    # need to do if values are equals to sky's regret 'em
    ret, thresh = cv2.threshold(blur, 226, 88, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    ## yeni skicit-image versiyonunda neighbors yerine connectivity kullanılmış
    ## neighbors = 8 iken, connectivity = 2 olarak değer laıyor
    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype='uint8')

    for label in np.unique(labels):
        # if this is the background label, ignore it (?)
        if label == 0:
            continue

        labelMask = np.zeros(thresh.shape, dtype='uint8')
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)

        # if the number of pixels in the component is sufficiently
        if numPixels > 300:
            mask = cv2.add(mask, labelMask)

    contours =  cv2.findContours(mask.copy() ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    # contours = imutils.grab_contours(contours)
    # contours = contours.sort_contours(contours)[0]
        # cv2.drawContours(frame, [c], -1, (0,255,0), 3)
    for i, c in enumerate(contours):
        # draw the bright spot on the image
        x, y, w, h = cv2.boundingRect(c)
        (cX, cY), radius = cv2.minEnclosingCircle(c)
 
        func(x, y, w, h)
        """
        if cv2.circle:
            print("fire #{} detected: x: {}, y: {}".format((i+1), int(cX), int(cY)))
        """

    # print('width, height: {}, {} '.format(width,height))
    # değerleri geri dön ya da direk olarak fonksiyon içinde kullan
    # return width, height
        # servos.Servos(width, height, int(cX), int(cY))

    # Display the resulting frame
    # cv2.flip(frame, -1)
    cv2.imshow('frame', frame)
    # cv2.imshow('frame', fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
