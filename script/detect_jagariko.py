#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, MultiArrayDimension

import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import random as rng

from converter import numpy2f32multi

class jagariko:
    def __init__(self):
        self.bridge = CvBridge()
        self.spot = []

    def img_callback(self, data):
        try:
            cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        output_img, mc = self.detect_moment(cv_img)

        try:
            self.pub_detect_img.publish(self.bridge.cv2_to_imgmsg(output_img, "mono8"))
        except CvBridgeError as e:
            print(e)

        if len(mc) != 0:
            data = numpy2f32multi(mc)
            self.pub_mc.publish(data)

        

    def detect_moment(self, img):
        #bgrのいずれかでグレースケール化（床色に合わせて変えよう）
        img_red = img[:, :, 2]
        #uint8がmono8(CV_8UC1[8bitのunsigned charの1列])に対応
        img_thresh = np.where(img_red > 80, 255, 0)
        img_thresh = np.array(img_thresh, dtype="uint8")
        #モルフォロジー変換
        kernel = np.ones((30,30),np.uint8)
        img_closing = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
        #ラベリング、中心抽出
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(img_closing)
        
        for i in range(1, len(centroids)):
            cv2.circle(img_closing, (int(centroids[i][0]), int(centroids[i][1])), 4, 100, 2, 4)

        mc = centroids[1:][:]#たぶん一番目が床
        center = np.array(np.shape(img_closing))/2
        mc = mc - center
        # print(mc)


        return img_closing, mc
        
    # 輪郭抽出(contours)が重いと思われる
    def detect_contours(self, img):
        #bgrのいずれかでグレースケール化（床色に合わせて変えよう）
        img_red = img[:, :, 2]
        #uint8がmono8(CV_8UC1[8bitのunsigned charの1列])に対応
        img_thresh = np.where(img_red > 110, 255, 0)
        img_thresh = np.array(img_thresh, dtype="uint8")
        #モルフォロジー変換
        kernel = np.ones((20,20),np.uint8)
        img_closing = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
        #輪郭抽出
        contours, hierarchy = cv2.findContours(img_closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get the moments
        mu = [None]*len(contours)
        for i in range(len(contours)):
            mu[i] = cv2.moments(contours[i])
            # Get the mass centers
            mc = [None]*len(contours)
            # add 1e-5 to avoid division by zero
            mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
            cv2.circle(img, (int(mc[i][0]), int(mc[i][1])), 4, 100, 2, 4)

        # print(mc)
        mc_bool = mc != None
        # mc_cut = mc[mc != None]
        print(mc_bool)

        return img#, mc_cut

    def main(self):
        rospy.init_node('detect_jagariko', anonymous=True)
        self.pub_detect_img = rospy.Publisher('detect_image', Image, queue_size=10)
        self.pub_mc = rospy.Publisher('mc', Float32MultiArray, queue_size=10)

        self.sub_img = rospy.Subscriber("image_raw", Image, self.img_callback)

        r=rospy.Rate(10)
        while not rospy.is_shutdown():
            None


if __name__ == '__main__':
    myjaga = jagariko()
    try:
        myjaga.main()
    except rospy.ROSInterruptException: pass