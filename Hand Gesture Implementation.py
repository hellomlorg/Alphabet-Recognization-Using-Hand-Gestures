#Author : Shivansh Joshi
# # Alphabet recognition Implementation

# ### Libraries needed

from collections import deque
import numpy as np
import cv2 
from keras.models import load_model
import pyttsx3
engine = pyttsx3.init()
 


# ### Important variables used in prgm



model = load_model('best_model.h5')  #loadig the ocr model created earlier
letters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l',
           12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w',
           23: 'x', 24: 'y', 25: 'z', 26: ''}
redLower = np.array([170, 100, 60])
redUpper = np.array([180, 255, 255]) # we can set this from the chart given in stack overflow

kernel = np.ones((5, 5), np.uint8)

# define blackboard and alphabets
blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
alphabet = np.zeros((200, 200, 3), dtype=np.uint8)
points = deque(maxlen=512)
sounddict={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,
          'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}


counter=0
cap = cv2.VideoCapture(0) # camera object
prediction = 26


# ### Camera working ( main steps )

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # so that we can see the proper image while moving our pen  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # changing the original frame to hsv
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # changing the original frame to grayscale
    
    # Detecting which pixel value falls under red color boundaries
    red = cv2.inRange(hsv, redLower, redUpper)
    
#     cv2.imshow("Initial InRange Image",red)

    # Preprocessing the input inRange Image
    red = cv2.erode(red, kernel)# erosion
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel) # opening
    red = cv2.dilate(red, kernel)# dilation
    
    cv2.imshow("red",red)

    # find countours in the image
    cnts, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #debug
    a=cv2.cvtColor(red,cv2.COLOR_GRAY2BGR)
    cv2.drawContours(a, cnts, -1, (0, 255, 0), 3) 
    cv2.imshow("Drawing contour",a)
    
    center = None
    # if any countours were found
    if len(cnts) > 0:
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y),), int(radius), (125, 344, 278), 2)
        
        
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        points.appendleft(center)
    # if no countours were found means if there is no red coloured object in the frame.
    elif len(cnts) == 0:
        if len(points) != 0:  #if there are points in deque and we have removed the pen . 
            blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(blackboard_gray, 15)
            blur = cv2.GaussianBlur(blur, (5, 5), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            cv2.imshow("Thresh", thresh)
            blackboard_cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
            
            #debug
            bb=cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
            cv2.drawContours(bb, blackboard_cnts, -1, (0, 255, 0), 3) 
            cv2.imshow("final_thresh_with_contour",bb)

            if len(blackboard_cnts) >= 1:
                cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]  # first sort all the contours and find the biggest contour

                if cv2.contourArea(cnt) > 1000: # I area of the selected countour is greater than 1000 , to maintain that there is no noise selected as countour.
                    x, y, w, h = cv2.boundingRect(cnt)
                    alphabet = blackboard_gray[y - 10:y + h + 10, x - 10:x + w + 10]
                    try:
                        img = cv2.resize(alphabet, (28, 28))
                        cv2.imshow("alphabet",alphabet)  # this is the alphabet image selected that we will give our OCR as an input . 
                    except cv2.error as e:
                        points = deque(maxlen=512)
                        blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
                        continue

                    img = np.array(img)
                    img = img.astype('float32') / 255
                    prediction = model.predict(img.reshape(1, 28, 28))[0]
                    prediction = np.argmax(prediction)
                    # try catch for sound 
                    try:
                        engine.setProperty('rate', 138)     # setting up new voice rate
                        volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
                        engine.setProperty('volume',0.5) 
                        engine.say("Our model Predicted the alphabet as")
                        engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
                        engine.say(str(letters[int(prediction)]))
                        print("Our model Predicted the alphabet as "+str(letters[int(prediction)]))
                        engine.runAndWait()
                    except Exception as e:
                        print("There is error in text to speech")

            # Empty the point deque and also blackboard
            points = deque(maxlen=512)
            blackboard = np.zeros((480, 640, 3), dtype=np.uint8)

    # connect the detected points with line
    for i in range(1, len(points)):
        if points[i - 1] is None or points[i] is None:
            continue
        cv2.line(frame, points[i - 1], points[i], (0, 0, 0), 2)
        cv2.line(blackboard, points[i - 1], points[i], (255, 255, 255), 8)

    cv2.putText(frame, "Prediction: " + str(letters[int(prediction)]), (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)
    cv2.imshow("Alphabet Recognition System", frame)
    if cv2.waitKey(5) == 13:  # if I press Enter it will break 
        break
cap.release()
cv2.destroyAllWindows()



