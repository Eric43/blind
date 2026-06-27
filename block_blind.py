"""
This is a method originally part of a larger function however this does not require any form of AI and maybe used independantly if an AI envrinoment.
Additional changes include the use of polyfill instead of rectangle to allow for more complex header shapes for blinding.  Will keep the "auto blind" to blind a percentage of the header.

"""

def block_blind(img_src='test_img.png',
                blind_block = ([[0,0],[1280, 0],[1280,48],[0,108]],),
                ): # header block = ~8.4% y max

    import cv2
    import numpy as np

    img = cv2.imread(img_src, cv2.IMREAD_COLOR)

    for block in blind_block:
        img = cv2.fillPoly(img, np.array([block]), (0,0,0))

    #end for loop (will change in future but just to inspect initial function)
    cv2.imshow("Block Blind inspection window", img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


    #####Determine the image size and adjust width and height????

#### NOT ALL ARE 640x480 autosize can adjust block height.