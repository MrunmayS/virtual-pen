load_from_disk = True
import numpy as np
import cv2
import time

if load_from_disk:
    penval = np.load('E:\LD-QSTP\Week-5\penval_green_01.npy')

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
canvas = None
kernal = np.ones((5,5), np.uint8)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
noiseth = 800
obj = 'pen'
x1,y1 = 0, 0
print("Press P to start drawing\nE for erase\nC to Clear\nS to Save")
while(True):
    img_og = cap.read()[1]
    img_og = cv2.flip(img_og, 1)
    if canvas is None:
        canvas = np.zeros_like(img_og)

    hsv = cv2.cvtColor(img_og, cv2.COLOR_BGR2HSV)

    lower_range = penval[0]
    upper_range = penval[1]

    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, kernal, iterations = 1)
    mask = cv2.dilate(mask, kernal, iterations = 2)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    key = cv2.waitKey(1)
    if key == ord('p'):
        obj = 'pen'
    if key == ord('e'):
        obj = 'eraser'
    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
        c = max(contours, key = cv2.contourArea)
        x2,y2,w,h = cv2.boundingRect(c)
        x3 = int((2*x2 + w)/2)
        y3 = int((2*y2 + h)/2)
        area = cv2.contourArea(c)
        if x1 == 0 and y1 ==0:
            x1, y1 = x3, y3
        else: 
            if obj == 'pen':
                canvas = cv2.line(canvas, (x1,y1),(x3,y3),[0, 0, 255],5)
            else:
                cv2.circle(canvas, (int((x2+x2+w)/2),int((y2+y2+h)/2)), 20, (0,0,0), -1)
        x1, y1 = x3, y3

        #cv2.rectangle(img_og, (x2,y2), (x2+w,y2+h), (25,25,255),2)

    else:
        x1, y1 = 0, 0
    key1 = cv2.waitKey(1)
    if key1 == ord('p'):
        obj = 'pen'
    if key1 == ord('e'):
        obj = 'eraser'
    
    img_og = cv2.add(img_og, canvas)

    cv2.imshow("pen", img_og)
    
    #key2 = cv2.waitKey(1)
    if key1 == 27:
        break
    if key1 == ord('s'):
        time.sleep(2)
        cv2.imwrite('img_01'+'.jpg',img_og)
        break
    if key1 == ord('c'):
        time.sleep(2)
        canvas = None
        clear = False
cv2.destroyAllWindows()
cap.release()