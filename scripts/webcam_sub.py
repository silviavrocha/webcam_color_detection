#!/usr/bin/env python3
# Description:
# - Subscribes to real-time streaming video from your built-in webcam.
#
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
 
# Import the necessary libraries
import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np

def callback(data):
 
  # Used to convert between ROS and OpenCV images
  br = CvBridge()
 
  # Output debugging information to the terminal
  rospy.loginfo("receiving video frame")
   
  # Convert ROS Image message to OpenCV image
  current_frame = br.imgmsg_to_cv2(data)
   
  # Display image
  #cv2.imshow("camera", current_frame)
   

  # Reading the video from the 
  # webcam in image frames 
  imageFrame = current_frame 

  # Convert the imageFrame in  
  # BGR(RGB color space) to  
  # HSV(hue-saturation-value) 
  # color space 
  hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

  # Set range for red color and  
  # define mask 
  red_lower = np.array([136, 87, 111], np.uint8) 
  red_upper = np.array([180, 255, 255], np.uint8) 
  red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

  # Set range for green color and  
  # define mask 
  green_lower = np.array([40, 100, 50], np.uint8) 
  green_upper = np.array([100, 255, 255], np.uint8) 
  green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

  # Set range for blue color and 
  # define mask 
  blue_lower = np.array([100,150,0], np.uint8) 
  blue_upper = np.array([140,255,255], np.uint8) 
  blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
    
  # Morphological Transform, Dilation 
  # for each color and bitwise_and operator 
  # between imageFrame and mask determines 
  # to detect only that particular color 
  kernal = np.ones((5, 5), "uint8") 
    
  # For red color 
  red_mask = cv2.dilate(red_mask, kernal) 
  res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                            mask = red_mask) 
    
  # For green color 
  green_mask = cv2.dilate(green_mask, kernal) 
  res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = green_mask) 
    
  # For blue color 
  blue_mask = cv2.dilate(blue_mask, kernal) 
  res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = blue_mask) 
  
  # Creating contour to track red color 
  contours, hierarchy = cv2.findContours(red_mask, 
                                          cv2.RETR_TREE, 
                                          cv2.CHAIN_APPROX_SIMPLE) 
    
  for pic, contour in enumerate(contours): 
      area = cv2.contourArea(contour) 
      if(area > 300): 
          x, y, w, h = cv2.boundingRect(contour) 
          imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                      (x + w, y + h),  
                                      (0, 0, 255), 2) 
            
          cv2.putText(imageFrame, "Red Colour", (x, y), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                      (0, 0, 255))     

  # Creating contour to track green color 
  contours, hierarchy = cv2.findContours(green_mask, 
                                          cv2.RETR_TREE, 
                                          cv2.CHAIN_APPROX_SIMPLE) 
    
  for pic, contour in enumerate(contours): 
      area = cv2.contourArea(contour) 
      if(area > 300): 
          x, y, w, h = cv2.boundingRect(contour) 
          imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                      (x + w, y + h), 
                                      (0, 255, 0), 2) 
            
          cv2.putText(imageFrame, "Green Colour", (x, y), 
                      cv2.FONT_HERSHEY_SIMPLEX,  
                      1.0, (0, 255, 0)) 

  # Creating contour to track blue color 
  contours, hierarchy = cv2.findContours(blue_mask, 
                                          cv2.RETR_TREE, 
                                          cv2.CHAIN_APPROX_SIMPLE) 
  for pic, contour in enumerate(contours): 
      area = cv2.contourArea(contour) 
      if(area > 300): 
          x, y, w, h = cv2.boundingRect(contour) 
          imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                      (x + w, y + h), 
                                      (255, 0, 0), 2) 
            
          cv2.putText(imageFrame, "Blue Colour", (x, y), 
                      cv2.FONT_HERSHEY_SIMPLEX, 
                      1.0, (255, 0, 0)) 
            
  # Program Termination 
  cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
  if cv2.waitKey(10) & 0xFF == ord('q'): 
      cap.release() 
      cv2.destroyAllWindows() 

  cv2.waitKey(1)
      
def receive_message():
 
  # Tells rospy the name of the node.
  # Anonymous = True makes sure the node has a unique name. Random
  # numbers are added to the end of the name. 
  rospy.init_node('video_sub_py', anonymous=True)
   
  # Node is subscribing to the video_frames topic
  rospy.Subscriber('video_frames', Image, callback)
 
  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()
 
  # Close down the video stream when done
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  receive_message()
