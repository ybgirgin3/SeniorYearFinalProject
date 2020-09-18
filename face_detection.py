import cv2

#cap = cv2.VideoCapture(0)
frame = cv2.imread('face.jpg')

face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')

# Our operations on the frame come here
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
# print(len(faces))
# Display the resulting frame
for (x,y,w,h) in faces:
     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
     """
     roi_gray = gray[y:y+h, x:x+w]
     roi_color = frame[y:y+h, x:x+w]
     eyes = eye_cascade.detectMultiScale(roi_gray)
     for (ex,ey,ew,eh) in eyes:
	 cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    """

cv2.imwrite('frame.png',frame)

# When everything done, release the capture
