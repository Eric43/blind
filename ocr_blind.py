
"""
Using the easyocr in pytorch to blind like the
work done in JUIM publication.

See easyOCR for more information on current language support!

Methods are:

easyOCR_block, this fills the detected boxes black.

easyOCR_poly_inpaint, this uses inpaint instead of black.

easyOCR_line_inpaint, this use the line method with inpaint
as described in KerasOCR examples and used in the prior publication.

The default values for the easyOCR readtext have been changed
from default and may need further tweaking. For blinding.

Currently used:
text_threshold=0.5,low_text=0.25,min_size=6.  26June26

This function differes from the OG publication by changing to easyOCR
but the underlying detection model (CRAFT(?REF?)) basically remain the same.

"""

import cv2
import easyocr
import numpy as np
import math

#TODO finish testing and adding easier **kwargs for easyOCR mods

def midpoint(x1, y1, x2, y2):
    """Support function used in the line_inpaint method"""
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)

    return (x_mid, y_mid)
## methods are:  easyOCR_block, easyOCR_poly_inpaint and easyOCR_line_inpaint
method = "easyOCR_line_inpaint"
# This needs to run only once to load the model into memory
reader = easyocr.Reader(['en'])

# reading the image
img = cv2.imread('test_img.png')
#Set the mask for inpaint etc.  may make conditional
mask = np.zeros(img.shape[:2], dtype="uint8")
# run OCR
results = reader.readtext(img,
                          text_threshold=0.5,
                          low_text=0.25,
                          min_size=6,
                          )

print(len(results))

# show the image and plot the results
#plt.imshow(img)
for res in results:
    # bbox coordinates of the detected text used for legacy method
    xy = res[0]
    xy0, xy1, xy2, xy3 = xy[0], xy[1], xy[2], xy[3]
    # text results and confidence of detection
    # Not assigning the detected words etc.  May use later saving (for now).
    # det, conf = res[1], res[2]
    #To do black (or color only fill)

    match method:
        case 'easyOCR_block':
            img = cv2.fillPoly(img, pts= np.asarray([xy]), color=(0, 0, 0))
        case 'easyOCR_poly_inpaint':
            cv2.fillPoly(mask, pts=np.asarray([xy]), color = 255)
            # Could probably just make a mask and inpaint all at the end.
            img = cv2.inpaint(img, mask, 2.71828, cv2.INPAINT_NS)
        case 'easyOCR_line_inpaint':
            #This is the method published in 2024 in Calhoun et al.
            x_mid0, y_mid0 = midpoint(xy1[0], xy1[1], xy2[0], xy2[1])
            x_mid1, y_mid1 = midpoint(xy0[0], xy0[1], xy3[0], xy3[1])
            thickness = int(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2 ))
            ## Using openCV to inpaint the identified text
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255,thickness)
            img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
        case _:
            print('The method chosen is not recognized: ', method)
            #mayneed to return an error for the API
            img = mask #Basically removing the img because it may contain data
            exit()

#At this point return the image

#end for loop
"""cv2.imshow("blind", img)

# wait for the user to press any key to exit window
cv2.waitKey(0)
"""
