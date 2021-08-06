import socket
import pickle
from cv2 import cv2
import numpy as np
import base64
import io
from io import BytesIO
from imageio import imread
import ffmpeg
from PIL import Image

def drow_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1],1), dtype=np.uint8)
    i=0
    try:
        for line in lines:
            print(f'line{i}={line}')
            for x1, y1, x2, y2 in line:
                print(f'x1={x1},x2={x2},y1={y1},y2={y2}')
                cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=10)
            i=i+1
        print(f'number of lines detected={i}')
    except TypeError:
        print('No lane lines detected')

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>95:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            
            
def compute_steering_angle(lines):
    
    try:
        if len(lines) == 1:
            print('Only detected one lane line' + str(lines[0]))
            x1, _, x2, _ = lines[0][0]
            x_offset = x2 - x1
        else:
            _, _, left_x2, _ = lines[0][0]
            _, _, right_x2, _ = lines[1][0]
            camera_mid_offset_percent = 0.02  
            mid = int(img.shape[1] / 2 * (1 + camera_mid_offset_percent))
            x_offset = ((left_x2 + right_x2) / 2) - mid
        y_offset = img.shape[0]
        angle_to_mid_radian = np.arctan(x_offset / y_offset)  
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / np.pi) 
        steering_angle = angle_to_mid_deg + 90  
        angle = steering_angle
        print(f'new steering angle: {str(angle)}')
        if (angle < 85) :
                print("R") 
                order=str("R")
        elif (angle >= 110 ):
            print("L") 
            order=str("L")  
        elif (angle >= 85 and angle <= 110):
            print("F")
            order=str("F")
        return order 
    except TypeError:
        print('stay on your direction ')
        order=str("F")
        return order


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.43.198', 8800))
serv.listen(5)
c=4
while True:
    conn, addr = serv.accept()
    from_client = ''
    data=[]
    remaining = int.from_bytes(conn.recv(4), 'big')
    while remaining:
        rbuf = conn.recv(min(remaining, 4096))
        remaining -= len(rbuf)
        data.append(rbuf)
    data_arr = pickle.loads(b"".join(data))
    print(data_arr)
    img=data_arr  
    imgContour = img.copy()
    imgGray=img
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny = cv2.Canny(imgBlur,70,70)
    getContours(imgCanny)
    imgBlank = np.zeros_like(img)
    lines = cv2.HoughLinesP(imgCanny,
                                rho=4,
                                theta=np.pi/180,
                                threshold=160,
                                lines=np.array([]),
                                minLineLength=2,
                                maxLineGap=25)
    image_with_lines = drow_the_lines(imgContour, lines)
    ORDER=compute_steering_angle(lines)
    msg =ORDER.encode('utf-8')
    conn.send(msg)
    print(ORDER)
    conn.close()
    print ('client disconnected')
    imgstack=stackImages(0.8,([image_with_lines],[imgCanny]))
    cv2.imshow('img',imgstack)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()