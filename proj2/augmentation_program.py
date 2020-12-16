import argparse
import cv2
import numpy as np
import glob
import os
import math
import json
import sys

import make_transforms

def checkmode(value):
    ivalue = int(value)
    if not (ivalue == 1 or ivalue == 2):
        raise argparse.ArgumentTypeError("%s is not in the rating range" % value)
    return ivalue 


def findHomography(image_1_kp, image_2_kp, matchs):
    image_1_points = np.zeros((len(matchs), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matchs), 1, 2), dtype=np.float32)

    for i in range(0, len(matchs)):
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
    mtx = np.load('preparation/camera_calibration/matrix.npy')
    dist = np.load('preparation/camera_calibration/distance_coefs.npy')
    return mtx, dist

def generate_solvePNP_points(image, homography, x_sections, y_sections):
    
    vertices = []
    obj_points = []

    x_increment = image.shape[1] / x_sections
    y_increment = image.shape[0] / y_sections

    for x in xrange(0, x_sections):

        for y in xrange(0, y_sections):

            vertices.append([x*x_increment, y*y_increment])

    return vertices, obj_points

def draw_rating(rating, image, image2, rvec, tvec, mtx, dist):
    for x in range(rating):
        width = min(image2.shape[1], image2.shape[0])*0.15
        draw_cube_title(image, rvec, tvec, mtx, dist, image2.shape[1]*0.5, image2.shape[0]*0.5, width=width, z=x, zgap=width*0.2)

def create_trans_im(width, height, name):
    #create 3 separate BGRA images as our "layers"
    layer = np.zeros((width, height, 3))

    cv2.putText(layer, name, (int(height*0.05), int(width*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 4, cv2.LINE_AA)

    if mode == 3:
        cv2.imshow("out.png", layer)
    
    return layer

def draw_cube_title(image, rvec, tvec, mtx, dist, dx=0, dy=0, width=200, z=0, zgap=20):
    dx -= width/2
    dy -= width/2

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

    #try:
    for n in range(imgpts.shape[0]):
        if abs(imgpts[n][0][0]) >= image.shape[0]*20 or abs(imgpts[n][0][1]) >= image.shape[1]*20:
            return

    cv2.fillConvexPoly(image, np.int32([imgpts[0], imgpts[1], imgpts[2], imgpts[3]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[4], imgpts[5], imgpts[6], imgpts[7]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[0], imgpts[1], imgpts[5], imgpts[4]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[1], imgpts[2], imgpts[6], imgpts[5]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[2], imgpts[3], imgpts[7], imgpts[6]]), (z * 40, z * 40, z * 40))
    cv2.fillConvexPoly(image, np.int32([imgpts[3], imgpts[0], imgpts[4], imgpts[7]]), (z * 40, z * 40, z * 40))

    # Draw pillars
    for i in range(0, 4):
        j = i+4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]),(255,0,0),1)

    # Draw bottom
    for i in range(0, 4):
        j = (i+1)%4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]),(0,255,),1)

    # Draw top
    for i in range(0, 4):
        j = (i+1)%4
        i = i+4
        j = j+4
        cv2.line(image, tuple(imgpts[i][0]), tuple(imgpts[j][0]), (0,0,255), 1)

def compute_frame(img2):

    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    # matcher takes normType, which is set to cv2.NORM_L2 for SIFT and SURF, cv2.NORM_HAMMING for ORB, FAST and BRIEF
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)
    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    good = [m for m, n in matches if m.distance < 0.7*n.distance]

    if mode == 3:
        print('Number of good matches: ')
        print(len(good))

    match_img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [good], None,
                                matchColor=(0, 255, 0), matchesMask=None,
                                singlePointColor=(255, 0, 0), flags=0)


    if mode == 3:
        cv2.imshow("im", match_img)
        cv2.waitKey(0)

    homography, mask = findHomography(kp1, kp2, good)

    vertices = np.float32([
        [0, 0],
        [0, img1.shape[0]],
        [img1.shape[1], img1.shape[0]],
        [img1.shape[1], 0],

    ]).reshape(-1,1,2)

    if(homography is not None):
        dst = cv2.perspectiveTransform(vertices, homography)
        img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3)

        obj_points = np.float32([
            [0, 0, 0],
            [0, img1.shape[0], 0],
            [img1.shape[1], img1.shape[0], 0],
            [img1.shape[1], 0, 0],
        ])

        retval, rvec, tvec, inliers = cv2.solvePnPRansac(obj_points, dst, mtx, dist)

        # Draw cubes & title
        draw_rating(rating, img2, img1, rvec, tvec)

        textimg = create_trans_im(img1.shape[0], img1.shape[1], movie_name)
        cv2.fillPoly(mask, [np.int32(dst)], (255,255,255))
        imgWarp = cv2.warpPerspective(textimg, homography, (img2.shape[1], img2.shape[0]))

        for x in range(img2.shape[0]):
            for y in range(img2.shape[1]):
                if(imgWarp[x][y][0] == 255 and imgWarp[x][y][1] == 0 and imgWarp[x][y][2] == 0):
                    img2[x][y] = (255,0,0)
    else:
        print("Homography detection error")

    #cv2.imshow('img2', img2)

def run_tutorial():

    mtx, dist = calibrate_camera()

    movie_name="dunkirk"
    file_name="dunkirk.jpg"

    img1 = cv2.imread('preparation/' + movie_name + '/' + file_name)

    print("1º passo: Identify features in the original image and match with the camera image to get the homography matrix")

    make_transforms.run(None, 'dunkirk.jpg', "tutorial", 3, None)
    make_transforms.run(True, None, None, None, "checkerboard2")

    img2 = cv2.imread("images/dunkirk_test.jpg")


    with open('preparation/' + movie_name + '/movie_data.txt', 'r') as movie_info:
        movie_infoList = json.load(movie_info)

    if mode == 3:
        print("Movie information present in descriptor: ")
        print(movie_infoList)

    rating = movie_infoList['movie_rating']
    name = movie_infoList['movie_name']

    detector = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    # matcher takes normType, which is set to cv2.NORM_L2 for SIFT and SURF, cv2.NORM_HAMMING for ORB, FAST and BRIEF
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)
    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    good = [m for m, n in matches if m.distance < 0.7*n.distance]

    if mode == 3:
        print('Number of good matches: ')
        print(len(good))

    match_img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [good], None,
                                matchColor=(0, 255, 0), matchesMask=None,
                                singlePointColor=(255, 0, 0), flags=0)


    if mode == 2:
        cv2.imshow("im", match_img)
        cv2.waitKey(0)
        cv2.destroyWindow("im")

    homography, mask = findHomography(kp1, kp2, good)

    vertices = np.float32([
        [0, 0],
        [0, img1.shape[0]],
        [img1.shape[1], img1.shape[0]],
        [img1.shape[1], 0],

    ]).reshape(-1,1,2)

    if(homography is not None):
        dst = cv2.perspectiveTransform(vertices, homography)
        img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3)

        print("2º passo: Use the homography matrix to get the image bounds in the camera image to solve the PnP problem")
        cv2.imshow("img", img2)
        cv2.waitKey(0)
        cv2.destroyWindow("img")

        obj_points = np.float32([
            [0, 0, 0],
            [0, img1.shape[0], 0],
            [img1.shape[1], img1.shape[0], 0],
            [img1.shape[1], 0, 0],
        ])

        retval, rvec, tvec, inliers = cv2.solvePnPRansac(obj_points, dst, mtx, dist)

        # Draw cubes & title
        draw_rating(rating, img2, img1, rvec, tvec, mtx, dist)

        textimg = create_trans_im(img1.shape[0], img1.shape[1], movie_name)
        cv2.fillPoly(mask, [np.int32(dst)], (255,255,255))
        imgWarp = cv2.warpPerspective(textimg, homography, (img2.shape[1], img2.shape[0]))

        for x in range(img2.shape[0]):
            for y in range(img2.shape[1]):
                if(imgWarp[x][y][0] == 255 and imgWarp[x][y][1] == 0 and imgWarp[x][y][2] == 0):
                    img2[x][y] = (255,0,0)

        print("3º passo: Use the translation and rotation matrices to correctly position the cubes on the scene")
        cv2.imshow('img', img2)
        cv2.waitKey(0)
        cv2.destroyWindow("img")

    else:
        print("Homography detection error")




def run_realtime():
    mtx, dist = calibrate_camera()

    img1 = cv2.imread('preparation/' + movie_name + '/' + file_name)

    if mode == 3 and img1 is not None:
        print('\n\nFound ' + file_name + ' in database')

    elif img1 is None:
        print(file_name + ' does not exist in our database. Please insert another title.')
        exit(0)

    with open('preparation/' + movie_name + '/movie_data.txt', 'r') as movie_info:
        movie_infoList = json.load(movie_info)

        if mode == 3:
            print("Movie information present in descriptor: ")
            print(movie_infoList)

    rating = movie_infoList['movie_rating']
    name = movie_infoList['movie_name']

    detector = cv2.xfeatures2d.SIFT_create()

    cv2.namedWindow("camera")
    vc = cv2.VideoCapture(0)
    startAugmenting = False

    FRAMES_PER_SEC = 15

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("camera", frame)
        rval, frame = vc.read()
        
        if startAugmenting:
            compute_frame(frame)
        
        key = cv2.waitKey(10)
        if key == 32: # Start augmentation on space
            startAugmenting = True
        if key == 27: # exit on ESC
            break
        cv2.waitKey(int(1000/FRAMES_PER_SEC))


# Arguments parsing
parser = argparse.ArgumentParser(description='Acquire an image, show the name of the movie and cubes representing the movie\'s rating')
parser.add_argument('-n', type=str, help='-n for file name')
parser.add_argument('-m', type=checkmode, help='-m for two possible working modes: 1 - normal mode | 2 - tutorial mode')
args = parser.parse_args()

mode = args.m

if mode == 2:
    run_tutorial()
else:
    
    if args.n is None or args.m is None:
        print("You must provide the movie (-n flag) and the mode (-m)")
        exit(0)

    file_name = args.n
    movie_name = os.path.splitext(args.n)[0]
    extension = os.path.splitext(args.n)[1]


    run_realtime()



cv2.destroyAllWindows()
