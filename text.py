from fun_code import *
#IMPORTS ENDS

# load image and converting it to read contours
while True:
    img = read_img('12.jpeg')                                                                   # reading image


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converting it to grey
    ret, thresh = cv2.threshold(gray, 1000, 200, cv2.THRESH_OTSU, cv2.THRESH_BINARY)            # appling threshold
    imgContours = img.copy()                                                                    # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy()                                                                  # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    # CALLING FUNCTIONS
    con = max_contours(contours)                                                                # CALLING CUT FUNCTION
    cv2.drawContours(imgContours, contours, con, (0, 255, 0), 5)                                # DRAW ALL DETECTED CONTOURS
    points = bounding(contours[con])                                                            # CALLING BOUNDRY FUNCTION
    drawRectangle(img,points, 1)                                                                # CALLING DRAY RECTANGLE FUNCTION
    final = prespective(points, img)
    bar_code = read_barcodes(img)
    gray2 = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    st,im = thresh1(gray2)
    array = text_transverse(st)
    print(array)


    cv2.imshow("data", im)

    cv2.waitKey(0)