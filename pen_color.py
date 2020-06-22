import cv2
import numpy as np
import time

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cv2.namedWindow("Trackbars")



cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while(True):
    
    img_og = cap.read()[1]
    img_og = cv2.flip(img_og, 1)
    hsv = cv2.cvtColor(img_og, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    
    mask = cv2.inRange(hsv, lower_range, upper_range)
    res = cv2.bitwise_and(img_og, img_og, mask=mask)
    mask_2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((mask_2, img_og, res))
    stacked = cv2.resize(stacked,None,fx=0.4,fy=0.4)
    cv2.imshow('video',stacked)
    #cv2.imshow('og', img_og)
    key = cv2.waitKey(1)
    if key == 27:
        break
      
    if key == ord('s'):
        
        arr1 = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
        print(arr1)
        
        np.save('penval_green_01', arr1)
        break

cap.release()
cv2.destroyAllWindows()