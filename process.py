import cv2
import numpy as np
import time

def process(image):
    image = cv2.resize(image, dsize=(0,0), fx=0.25, fy=0.25)
    image2 = image.copy()
    # image = cv2.flip(image, 0)
    hh, ww = image.shape[:2]
    lower = np.array([0, 0, 160]) # FIXME: tune for different cameras
    upper = np.array([100,255,255])  # FIXME: tune for different cameras

    image = cv2.GaussianBlur(image, (27,27),0)
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    # cv2.imwrite('filtered.png', result)

    imgray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(imgray, 0, 255, 0)
    
    canny = cv2.Canny(imgray, 20, 200)
    # cv2.imwrite('canny.png', canny)

    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                            param1=30, param2=15, minRadius=0, maxRadius=0)
    # print("circlies" + str(circles))

    result = image.copy()
    max_area = 0
    mx = 0
    my = 0
    mr = 0
    if circles is not None and circles.size > 0:
        for circle in circles[0]:
            # draw the circle in the output image
            (x,y,r) = circle
            x = int(x)
            y = int(y)
            r = int(r)
            if (r**2 > max_area):
                max_area = r**2
                mx = x
                my = y
                mr = r

        cv2.circle(image2, (mx, my), mr, (0, 0, 255), 1)

    cv2.imwrite('result.png', image2)
    # print(f'returning {mx}, {my}, {mr}, {ww}, {hh}')
    return mx, my, mr, ww, hh, image2



if __name__ == "__main__":
    process(cv2.imread("file.png"))
    