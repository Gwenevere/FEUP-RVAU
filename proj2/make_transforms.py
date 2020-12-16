import cv2
import argparse
import numpy as np
import os

def checkrating(value):
    ivalue = int(value)
    if not (ivalue<=5 and ivalue >=1):
        raise argparse.ArgumentTypeError("%s is not in the rating range" % value)
    return ivalue

parser = argparse.ArgumentParser(description='Read an image and make transforms and compute descriptors.')
parser.add_argument('image', type=str,
                    help='name of the image inside posters folder (with extension)')
parser.add_argument('name', type=str,
                    help='name of the movie')
parser.add_argument('name', type=checkrating,
                    help='rating of the movie (1-5)')
args = parser.parse_args()

image_name = os.path.splitext(args.image)[0]
extension = os.path.splitext(args.image)[1]
img = cv2.imread("posters/" + args.image)

if(img == None):
    print("No such image")
    exit(0)

cv2.imshow("image", img)
cv2.waitKey(0)

sift = cv2.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(img, None)

#orb = cv2.ORB_create(nfeatures=500)
#kp, des = orb.detectAndCompute(img, None)

img2 = cv2.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

cv2.imshow("keypoints", img2)
cv2.waitKey(0)


# Transformations
vertices = np.float32([
    [0, 0],
    [0, img.shape[0]],
    [img.shape[1], img.shape[0]],
    [img.shape[1], 0],
]).reshape(-1,1,2)

pts1 = np.float32([[img.shape[0]/2, img.shape[1]/2], [0, img.shape[1]/4 + img.shape[1]/2], [img.shape[0]/2, img.shape[1]], [img.shape[0], img.shape[1]/4 + img.shape[1]/2]])

M = cv2.getPerspectiveTransform(vertices, pts1)

dst = cv2.warpPerspective(img, M, (img.shape[0], img.shape[1]))

dst = cv2.resize(dst,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)

cv2.imshow("imgtransformed", dst)
cv2.waitKey(0)

if not os.path.exists('computed_posters/' + os.path.splitext(args.image)[0]):
    os.mkdir("computed_posters/" + os.path.splitext(args.image)[0])

np.save("computed_posters/" + image_name + "/descriptor", des)
cv2.imwrite("computed_posters/" + image_name + '/' + args.image, img)
cv2.imwrite("computed_posters/" + image_name + '/' + image_name + '2' + extension, dst)