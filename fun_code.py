import numpy as np
import cv2
import pytesseract
from pyzbar.pyzbar import decode

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


with open("data.txt") as f:
    myDataList = f.read().splitlines()
################################################################################################################################################
def read_img(path):
    img = cv2.imread(path)
    return img
################################################################################################################################################

################################################################################################################################################

def max_contours(contours):
    biggest = np.array([])
    max_area = 0
    for con in range(len(contours)):
        conture =contours[con]
        area = int(cv2.contourArea(conture))
        peri = cv2.arcLength(conture, True)
        approx = cv2.approxPolyDP(conture, 0.0001 * peri, True)
        if area >max_area:
            max_area = area
            biggest = conture
            conr =con

    return conr

################################################################################################################################################

################################################################################################################################################
def bounding(con):
    array = []
    for i in range(len(con)):
        x= con[i][0][0]
        y= con[i][0][1]
        array.append([x,y])
    max = -1
    min = 10000000000000
    for ind in range(len(array)):
        xval = array[ind][0]
        if xval < min :
            min = xval
        if xval>max :
            max = xval
    minx = min
    maxx= max
    max = -1
    min = 10000000000000
    for ind in range(len(array)):
        yval = array[ind][1]
        if yval < min :
            min = yval
        if yval>max :
            max = yval
    miny = min
    maxy = max
    array = [[minx,miny],[minx,maxy],[maxx,maxy],[maxx,miny]]

    return array

################################################################################################################################################

################################################################################################################################################

def drawRectangle(img, biggest, thickness):
    cv2.line(img, (biggest[0][0], biggest[0][1]), (biggest[1][0], biggest[1][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[0][0], biggest[0][1]), (biggest[3][0], biggest[3][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0], biggest[3][1]), (biggest[2][0], biggest[2][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[2][0], biggest[2][1]), (biggest[1][0], biggest[1][1]), (0, 255, 0), thickness)

################################################################################################################################################

################################################################################################################################################
def prespective(biggest,img):
    scale = 1
    pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
    highttrace = (biggest[1][1]-biggest[0][1])*scale
    widthtrace = (biggest[2][0]-biggest[0][0])*scale
    pts2 = np.float32([[0, 0],  [0, highttrace], [widthtrace, highttrace], [widthtrace, 0]])  # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthtrace, highttrace))
    return imgWarpColored
################################################################################################################################################

################################################################################################################################################
def decord_text(img):
    image = img
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    box = pytesseract.image_to_data(image)
    string =pytesseract.image_to_string(image)
    hight,width,_ =image.shape
    for x,a in enumerate(box.splitlines()):
        if x!=0:
            a = a.split()
            if len(a)==12:
                x,y,w,h = int(a[6]),int(a[7]),int(a[8]),int(a[9])
                cv2.rectangle(image,(x,y),(w+x,h+y),(255,0,0),3)
                cv2.putText(image,a[11], (x,y),cv2.FONT_HERSHEY_SIMPLEX,1, (50,50,255),2 )
    # cv2.imshow("image",image)
    # cv2.waitKey(0)
    return string,image

################################################################################################################################################

################################################################################################################################################
def read_barcodes(img):
    for barcode in decode(img):
        myData = barcode.data.decode("utf-8")
        print(myData)
        if myData in myDataList:
            myOutput = "Real Medicine"
            myColor = (0, 255, 0)
        else:
            myOutput = "Fake Medicine"
            myColor = (0, 0, 255)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)
    return img
###############################################################################################################################################


###############################################################################################################################################

def thresh1(gray_image):
    max_len = 0
    for i in range(11, 111, 10):
        adaptive_threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, i, 11)
        st, im = decord_text(adaptive_threshold)
        if len(st) > max_len:
            max_len = len(st)
            best = im
            bestst = st
    return bestst, best

###############################################################################################################################################
def text_transverse(text):
    array = []
    str = ""
    for i in range(len(text)):
        if text[i] =='\n':
            array.append(str)
            str = ""

        else:
            str = str + text[i]
    array2 = []


    for i in array:
        if len(i)==0:
            array2.append(i)
        for j in range(len(i)):
            if (i[j]  == " " and (j <len(i)-1)):
                continue
            elif(j == len(i)-1 and i[j] == " "):
                array2.append(i)

            else:
                break
    for i in array2:
        array.remove(i)


    return array




###############################################################################################################################################
