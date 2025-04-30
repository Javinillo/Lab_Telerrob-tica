#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def image_callback(msg):
    try:
        np_arr = np.frombuffer(msg.data, np.uint8)
        #image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # OpenCV >= 3.0
    except CvBridgeError as e:
        print(e)
    else:
        cv2.imshow('cv_img', image_np)
        cv2.waitKey(5)

def main():
    rospy.init_node('image_processing')
    image_topic = "/robot1921681092/compressedimage"
    rospy.Subscriber(image_topic, CompressedImage, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()


