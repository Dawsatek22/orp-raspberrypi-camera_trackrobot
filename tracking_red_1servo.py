# this is a code to track the red color with 1x mg996r servos and pi camera
from time import sleep # to use if i need to delay something
import cv2 # the opencv python module
import numpy as np
from picamera2 import Picamera2 # to use the webcam
 # to control the servo.for more info to setup link is here https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/
from adafruit_servokit import ServoKit

track = ServoKit(channels=16) # the object for the pwm channels

track.servo[0].set_pulse_width_range(1000,2000) # setting the pulse range

track.servo[0].angle = 90

# below are the setup for the picamera2 to use the raspberrt pi camera
picam2 = Picamera2()
picam2.preview_configuration.main.size=(1280, 720) #full screen : 3280 2464
picam2.preview_configuration.main.format = "RGB888" #8 bits
picam2.start()





while True:
    Frame = picam2.capture_array()
    rows, cols,_ = Frame.shape
    x_medium = int(cols / 2)
  
    center = int(cols / 2)
    position1 = 90 # start angle
    
	# Convert the imageFrame in 
	# BGR(RGB color space) to 
	# HSV(hue-saturation-value) 
	# color space 
    hsvFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV) 


	# Set range for red color and 
	# define mask 
    
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
	
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

 
	
	# Morphological Transform, Dilation 
	# for green color and bitwise_and operator 
	# between imageFrame and mask determines 
	# to detect only that particular color 
	
    kernel = np.ones((5, 5), "uint8") 
	
	
	# For red color 
	
    red_mask = cv2.dilate(red_mask, kernel) 
	
    res_red = cv2.bitwise_and(Frame, Frame, 
								mask = red_mask) 
	
    	# Creating contour to track red color 
	
    red_contours, hierarchy = cv2.findContours(red_mask, 
										cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, red_contour in enumerate(red_contours): 
        area = cv2.contourArea(red_contour) 
        if (area > 300): 
          x, y, w, h = cv2.boundingRect(red_contour) 
          x_medium = int(x + x + w/2)
          y_medium = int(y + y+ h/2)
          Frame = cv2.rectangle(Frame, (x, y), (x + w, y + h), 
									(0, 0, 255), 2) 
          cv2.putText(Frame, "red Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (0, 0, 255))
          
        else:
          print('red object is not detected')  
          
        
         # position is measured by x_medium values
          if x_medium < center -30:
            position1 -= 1
          elif x_medium > center + 30:
            position1 -= 1
        
          # limits for serv angle is set
          if position1 >= 180:
           position1 = 180

          if position1 <= 0:
           position1 = 0

          
        track.servo[0].angle = position1
        
        
                         
        
       
    
    cv2.line(Frame, (x_medium, 0), (x_medium,480), (0, 255, 0), 2)
    cv2.imshow("preview",Frame)
    if cv2.waitKey(1)==ord('q'): # q is for break
        break
picam2.stop()
cv2.destroyAllWindows()
	
