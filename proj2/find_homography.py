import argparse
import cv2
import numpy as np
import glob
import os
import math

def findHomography(image_1_kp, image_2_kp, matchs):
    image_1_points = np.zeros((len(matchs), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matchs), 1, 2), dtype=np.float32)

    for i in range(0, len(matchs)):
        #print("queryidx")
        #print(matchs[0][0])
        image_1_points[i] = image_1_kp[matchs[i].queryIdx].pt
        image_2_points[i] = image_2_kp[matchs[i].trainIdx].pt


    homography, mask = cv2.findHomography(image_1_points, image_2_points, cv2.RANSAC, ransacReprojThreshold=20.0)

    return homography, mask

def resize_to_image(src, destSizeImage):

    height, width = src.shape[:2]
    max_height, max_width = destSizeImage.shape[:2]

    # only shrink if src is bigger than required
    if max_height < height or max_width < width:
        # get scaling factor
        scaling_factor = max_height / float(height)
        if max_width/float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        # resize image
        dest = cv2.resize(src, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        return dest
    else:
        return src


def calibrate_camera():
        
    # Defining the dimensions of checkerboard
    CHECKERBOARD = (6,9)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = [] 


    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None

    # Extracting path of individual image stored in a given directory
    images = glob.glob('./images/checkerboard2/*.jpg')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            
            imgpoints.append(corners2)

            # img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            # img = cv2.resize(img, None, fx=700/img.shape[1], fy=700/img.shape[1])
            # cv2.imshow('img',img)
            # cv2.waitKey(0)

    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return ret, mtx, dist, rvecs, tvecs

def generate_solvePNP_points(image, homography, x_sections, y_sections):
    
    vertices = []
    obj_points = []

    x_increment = image.shape[1] / x_sections
    y_increment = image.shape[0] / y_sections

    for x in xrange(0, x_sections):

        for y in xrange(0, y_sections):

            vertices.append([x*x_increment, y*y_increment])

    
    #print(vertices)

    # vertices = np.float32([
    #     [0, 0],
    #     [0, img1.shape[0]],
    #     [img1.shape[1], img1.shape[0]],
    #     [img1.shape[1], 0],
    #     [img1.shape[0]/2, 0],
    #     [0, img1.shape[0]/2],
    #     [0, img1.shape[1]/2],
    #     [img1.shape[1]/2, 0],

    # ]).reshape(-1,1,2)


    # dst = cv2.perspectiveTransform(vertices, homography)
    # img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3)

    # obj_points = np.float32([
    #     [0, 0, 0],
    #     [0, img1.shape[0], 0],
    #     [img1.shape[1], img1.shape[0], 0],
    #     [img1.shape[1], 0, 0],
    #     [img1.shape[0]/2, 0, 0],
    #     [0, img1.shape[0]/2, 0],
    #     [0, img1.shape[1]/2, 0],
    #     [img1.shape[1]/2, 0, 0],
    # ])

    return vertices, obj_points


def draw_rating(rating, image, image2):
    for x in range(rating):
        draw_cube_title(image, "Dunkirk", image2.shape[1]*0.5, image2.shape[0]*0.5, z=x)

def create_trans_im(width, height, title):
    #create 3 separate BGRA images as our "layers"
    layer = np.zeros((width, height, 3))

    cv2.putText(layer, title, (int(height*0.05), int(width*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 5, cv2.LINE_AA)

    cv2.imshow("out.png", layer)
    
    return layer


def draw_cube_title(image, title_name="", dx=0, dy=0, width=200, z=0, zgap=50):
    dx -= width/2
    dy -= width/2

    print(z)

    axis = np.float32([[0 + dx, 0 + dy,-(width + zgap) * z], 
                       [0 + dx, width + dy,-(width + zgap) * z], 
                       [width + dx, width + dy,-(width + zgap) * z], 
                       [width + dx, 0 + dy,-(width + zgap) * z],
                       [0 + dx, 0 + dy,-width * (z + 1) - zgap * z],
                       [0 + dx, width + dy,-width * (z + 1) - zgap * z],
                       [width + dx, width + dy, -width * (z + 1) - zgap * z], 
                       [width + dx, 0 + dy,-width * (z + 1) - zgap * z] 
                    ]).reshape(-1,3)

    imgpts, jac = cv2.projectPoints(axis, rvec, tvec, mtx, dist)


    cv2.fillConvexPoly(image, np.int32([imgpts[0], imgpts[1], imgpts[2], imgpts[3]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[4], imgpts[5], imgpts[6], imgpts[7]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[0], imgpts[1], imgpts[5], imgpts[4]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[1], imgpts[2], imgpts[6], imgpts[5]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[2], imgpts[3], imgpts[7], imgpts[6]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[3], imgpts[0], imgpts[4], imgpts[7]]), (z * 40, z * 40, z * 40))


    # Draw pillars
    for i in range(0, 4):
        j = i+4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]),(255,0,0),3)

    # Draw bottom
    for i in range(0, 4):
        j = (i+1)%4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]),(0,255,),3)

    # Draw top
    for i in range(0, 4):
        j = (i+1)%4
        i = i+4
        j = j+4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]), (0,0,255), 3)
            

ret, mtx, dist, _, _ = calibrate_camera()

img1 = cv2.imread('computed_posters/poster4/poster4.jpg')
img2 = cv2.imread('computed_posters/poster4/poster44.jpg')
poster_name = "wefwrf"
#img1 = cv2.imread('posters/dunkirk.jpg')
#img2 = cv2.imread('images/hehexd3.jpg')
#poster_name = "Dunkirk"

#img1 = cv2.resize(img1, (int(img1.shape[1]*0.4), int(img1.shape[0]*0.4)))

#img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

#detector = cv2.ORB_create()
detector = cv2.xfeatures2d.SIFT_create()
kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

# matcher takes normType, which is set to cv2.NORM_L2 for SIFT and SURF, cv2.NORM_HAMMING for ORB, FAST and BRIEF
bf = cv2.BFMatcher()
matches = bf.match(des1, des2)
print(matches[0])
matches = bf.knnMatch(des1, des2, k=2)

good = []

good = [m for m, n in matches if m.distance < 0.7*n.distance]

print('Number of good matches: ')
print(len(good))

match_img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [good], None,
                            matchColor=(0, 255, 0), matchesMask=None,
                            singlePointColor=(255, 0, 0), flags=0)

#matches = sorted(matches, key=lambda x: x.distance)
#match_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None)

cv2.imshow("im", match_img)
cv2.waitKey(0)

homography, mask = findHomography(kp1, kp2, good)


vertices = np.float32([
    [0, 0],
    [0, img1.shape[0]],
    [img1.shape[1], img1.shape[0]],
    [img1.shape[1], 0],

]).reshape(-1,1,2)


dst = cv2.perspectiveTransform(vertices, homography)
img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3)

obj_points = np.float32([
    [0, 0, 0],
    [0, img1.shape[0], 0],
    [img1.shape[1], img1.shape[0], 0],
    [img1.shape[1], 0, 0],
])

retval, rvec, tvec, inliers = cv2.solvePnPRansac(obj_points, dst, mtx, dist)


# Draw axis

draw_rating(3, img2, img1)

textimg = create_trans_im(img1.shape[0], img1.shape[1], poster_name)

#mask = np.zeros(img1.shape[1], img1.shape[0], 4)

cv2.fillPoly(mask, [np.int32(dst)], (255,255,255))

imgWarp = cv2.warpPerspective(textimg, homography, (img2.shape[1], img2.shape[0]))

for x in range(img2.shape[0]):
    for y in range(img2.shape[1]):
        if(imgWarp[x][y][0] == 255 and imgWarp[x][y][1] == 0 and imgWarp[x][y][2] == 0):
            img2[x][y] = (255,0,0)

cv2.imshow('img2', img2)


# # img3 = cv2.imread('posters/kill_bill_vol1.jpg', 0)
# # img3 = resize_to_image(img3, img1)

# # imgWarp = cv2.warpPerspective(img3, homography, (img2.shape[1], img2.shape[0]))

# # # mask = np.zeros((img2.shape[0], img2.shape[1]), np.uint8)
# # # cv2.fillPoly(mask, [np.int32(dst)], (255,255,255))
# # # maskInverse = cv2.bitwise_not(mask)

# # # mask = img1.copy()
# # # mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
# # # mask.fill(0)
# # # poly = np.int32(dst)
# # # cv2.fillPoly(mask, [poly], 255)

# # # #create region of interest
# # # roi = img2[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]
# # # mask = mas[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]

# # # mask_inv = cv2.bitwise_not(mask)
# # # img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
# # # src1_cut = src1[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]


# # # imgAug = img2.copy()
# # # imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInverse)
# # # imgAug = cv2.bitwise_or(imgWarp, imgAug)

# # draw first 50 matches

# cv2.imshow('original', img1)
# cv2.imshow('real_world', img2)
# cv2.imshow('Matches', match_img)
# # cv2.imshow('augmentation', img3)
# # cv2.imshow('warp', imgWarp)
# # cv2.imshow('mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
