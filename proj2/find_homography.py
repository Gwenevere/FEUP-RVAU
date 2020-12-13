import argparse
import cv2
import numpy as np

def findHomography(image_1_kp, image_2_kp, matches):
    image_1_points = np.zeros((len(matches), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matches), 1, 2), dtype=np.float32)

    for i in range(0, len(matches)):
        image_1_points[i] = image_1_kp[matches[i].queryIdx].pt
        image_2_points[i] = image_2_kp[matches[i].trainIdx].pt


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

img1 = cv2.imread('posters/dunkirk.jpg', 0)

# img2 = cv2.imread('images/WIN_20201210_17_10_25_Pro.jpg', 0)
img2 = cv2.imread('images/hehexd2.jpg', 0)

img1 = cv2.resize(img1, (int(img1.shape[1]*0.4), int(img1.shape[0]*0.4)))

orb = cv2.ORB_create(nfeatures=500)
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# matcher takes normType, which is set to cv2.NORM_L2 for SIFT and SURF, cv2.NORM_HAMMING for ORB, FAST and BRIEF
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

match_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None)

    
homography, mask = findHomography(kp1, kp2, matches)


# print(homography)
# print(mask.shape)

vertices = np.float32([
    [0, 0],
    [0, img1.shape[0]],
    [img1.shape[1], img1.shape[0]],
    [img1.shape[1], 0]
]).reshape(-1,1,2)


dst = cv2.perspectiveTransform(vertices, homography)
img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3)



# cv2.solvePnP()


# img3 = cv2.imread('posters/kill_bill_vol1.jpg', 0)
# img3 = resize_to_image(img3, img1)

# imgWarp = cv2.warpPerspective(img3, homography, (img2.shape[1], img2.shape[0]))

# # mask = np.zeros((img2.shape[0], img2.shape[1]), np.uint8)
# # cv2.fillPoly(mask, [np.int32(dst)], (255,255,255))
# # maskInverse = cv2.bitwise_not(mask)

# # mask = img1.copy()
# # mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
# # mask.fill(0)
# # poly = np.int32(dst)
# # cv2.fillPoly(mask, [poly], 255)

# # #create region of interest
# # roi = img2[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]
# # mask = mas[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]

# # mask_inv = cv2.bitwise_not(mask)
# # img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
# # src1_cut = src1[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]


# # imgAug = img2.copy()
# # imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInverse)
# # imgAug = cv2.bitwise_or(imgWarp, imgAug)

# draw first 50 matches

cv2.imshow('original', img1)
cv2.imshow('real_world', img2)
cv2.imshow('Matches', match_img)
# cv2.imshow('augmentation', img3)
# cv2.imshow('warp', imgWarp)
# cv2.imshow('mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
