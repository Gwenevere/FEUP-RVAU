#!/usr/bin/env python

import numpy as np
import cv2 as cv
import glob
import os


# Defining the dimensions of checkerboard
CHECKERBOARD = (6,9)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 


# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
images = glob.glob('./images/*.jpg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
    
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

        vertices = np.array([
            [corners[0][0][0], corners[0][0][1]],
            [corners[0][0][0], corners[len(corners)-1][0][1]],
            [corners[len(corners)-1][0][0], corners[len(corners)-1][0][1]],
            [corners[len(corners)-1][0][0], corners[0][0][1]]
        ], np.int32)

        # cv.rectangle(img,(int(corners[0][0][0]), int(corners[0][0][1])),(int(corners[len(corners)-1][0][0]), int(corners[len(corners)-1][0][1])),(0,255,0),3)
        cv.polylines(img,[vertices],True,(0,255,0), 3)

    
    cv.imshow('img',img)
    cv.waitKey(0)

cv.destroyAllWindows()

h,w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\nCamera matrix :")
print(mtx)
print("\ndist :")
print(dist)
print("\nrvecs :")
print(rvecs[0])
print("\ntvecs :")
print(tvecs)
print("\nimgpoints :")
print(imgpoints[0][0])



'''
img = cv.imread('posters/dunkirk.jpg')
img = cv.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
print(img.shape)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
print("before")
sift = cv.xfeatures2d.SIFT_create()
print(gray.shape)
kp, des = sift.detectAndCompute(gray,None)
print("after")
gray = cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
print("afterr")
cv.imwrite('sift_keypoints.jpg', gray)
'''

cv.namedWindow("camera")
vc = cv.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv.imshow("camera", frame)
    rval, frame = vc.read()
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break
cv.destroyWindow("camera")
