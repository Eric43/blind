"""
This is a method originally part of a larger function however this does not require any form of AI and maybe used independently if an AI environment.
Additional changes include the use of polyfill instead of rectangle to allow for more complex header shapes for blinding.  Will keep the "auto blind" to blind a percentage of the header.

"""

def block_blind(img_src='test_img.png',
                blind_block = ([[0,0],[1280, 0],[1280,48],[0,108]],),
                auto_block = None,
                ): # header block 0.084 in fx

    import cv2
    import numpy as np

    img = cv2.imread(img_src, cv2.IMREAD_COLOR)

    if auto_block is None:
        for block in blind_block:
            img = cv2.fillPoly(img, np.array([block]), (0,0,0))
    elif auto_block > 0:
        """This sets the block at user defined
        (i.e. auto_block =0.084 or 8.4% of the image) at the header"""
        h, w, _ = img.shape
        xmin = 0
        ymin = 0
        xmax = w
        ymax = round(auto_block * h)
        img = cv2.rectangle(img, (xmin,ymin), (xmax, ymax), (0,0,0), -1)

    return img
