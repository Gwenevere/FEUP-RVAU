import cv2
import argparse
import numpy as np
import os
import json
import glob

PREPARATION_DIR= "preparation"
# Number of images to use for calibration
NUM_IMAGES_CALIB = 30
CALIB_FRAMES_PER_SEC = 5


def create_directories():
    if not os.path.exists(PREPARATION_DIR):
        os.mkdir(PREPARATION_DIR)
        print("Created ./preparation directory")

        

def camera_calibration(argCI):
        
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

    if argCI is None:
        
        cv2.namedWindow("camera")
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
        
        c = 0

        print("Show chessboard in different poses for calibration")

        while rval:
            cv2.putText(frame, "Show chessboard in different poses", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)
            cv2.imshow("camera", frame)
            rval, frame = vc.read()
            
            # Convert to grayscale for some reason
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(frame, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            drawn = cv2.drawChessboardCorners(frame, CHECKERBOARD, corners, ret)

            """
            If desired number of corner are detected,
            we refine the pixel coordinates and display
            them on the images of checker board
            """
            if ret == True:
                #cv2.imwrite("calib_test" + str(c) + ".jpg", frame)
                c = c+1
                objpoints.append(objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
                
                imgpoints.append(corners2)
            
            cv2.waitKey(int(1000/CALIB_FRAMES_PER_SEC))
            #computeFrame(frame)
            
            if c == NUM_IMAGES_CALIB:
                print()
                break
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
        cv2.destroyWindow("camera")

        """
        Performing camera calibration by 
        passing the value of known 3D points (objpointfs)
        and corresponding pixel coordinates of the
        detected corners (imgpoints)
        """
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        np.save(PREPARATION_DIR + "/camera_calibration/matrix", mtx)
        np.save(PREPARATION_DIR + "/camera_calibration/distance_coefs", dist)
        np.save(PREPARATION_DIR + "/camera_calibration/rvecs", np.array(rvecs))
        np.save(PREPARATION_DIR + "/camera_calibration/tvecs", np.array(tvecs))

    else:
        images = glob.glob('./images/' + str(argCI) + '/*.jpg')
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
            if ret == True:
                objpoints.append(objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
    
                imgpoints.append(corners2)
        
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        np.save(PREPARATION_DIR + "/camera_calibration/matrix", mtx)
        np.save(PREPARATION_DIR + "/camera_calibration/distance_coefs", dist)
        np.save(PREPARATION_DIR + "/camera_calibration/rvecs", np.array(rvecs))
        np.save(PREPARATION_DIR + "/camera_calibration/tvecs", np.array(tvecs))



def checkrating(value):
    ivalue = int(value)
    if not (ivalue<=5 and ivalue >=1):
        raise argparse.ArgumentTypeError("%s is not in the rating range" % value)
    return ivalue


def run(argC, argI, argN, argR, argCI):
    create_directories()

    if(not argC):
        if argI is None or argN is None or argR is None:
            print("You must provide the image (-i flag), the name of the movie (-n) and the rating (-r)")
            return
    else:
        camera_calibration(argCI)
        print("Camera calibrated with success")
        return

    # Uploading posters program
    image_name = os.path.splitext(argI)[0]

    extension = os.path.splitext(argI)[1]
    movie_name = argN
    movie_rating = argR
    img = cv2.imread("posters/" + argI)
    img2 = cv2.imread(argI)

    if img is None:
        if img2 is None:
            print("Image not found")
            return
        else:
            img = img2

    cv2.imshow("image", img)
    cv2.waitKey(0)

    # May conflict with the versions
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(img, None)

    img2 = cv2.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

    cv2.imshow("keypoints", img2)
    cv2.waitKey(0)

    # Create poster directory
    if not os.path.exists(PREPARATION_DIR+ '/' + os.path.splitext(argI)[0]):
        os.mkdir(PREPARATION_DIR + '/' + os.path.splitext(argI)[0])
        print("Created ./preparation/" + os.path.splitext(argI)[0] +  " directory")

    # Create JSON with movie info (name and rating)
    movie_info = {
        "movie_name" : movie_name,
        "movie_rating" : movie_rating
    }

    with open(PREPARATION_DIR + '/' + image_name + '/movie_data.txt', 'w+') as outfile:
        json.dump(movie_info, outfile)

    # Store image and descriptor
    np.save(PREPARATION_DIR + "/" + image_name + "/descriptor", movie_info)
    cv2.imwrite(PREPARATION_DIR + "/" + image_name + '/' + argI, img)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read an image, make transforms and compute descriptors.')
    parser.add_argument('-c', help='-c for calibration mode', action='store_true')
    parser.add_argument('-i', type=str,
                        help='name of the image inside posters folder (with extension)')
    parser.add_argument('-n', type=str,
                        help='name of the movie')
    parser.add_argument('-r', type=checkrating, help='rating of the movie (1-5)')
    parser.add_argument('-ci', type=str, help='Path of the calibration images. If this argument is missing, it is considered to be realtime camera images ')


    args = parser.parse_args()

    print(args.c)


    run(args.c, args.i, args.n, args.r, args.ci)
