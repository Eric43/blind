########################################
#### function to extract frames from ###
### An standard video file and save ####
#### to an png.  Will add blinding  ####
### And ability to select img type  ####
#### in the futures.  V. 0.1 alpha  ####
#### GPLv3 license fsf.org           ###
####  SynXBio Inc.  Written by:      ###
### Eric W. Olle  30 November 2023  ####
########################################


#### Working on for pytorch conversion.
def ocr_blind_vid(file_name,
                    file_path,
                    new_path = './frames',
                    img_prefix = '2v_',
                    img_class = '',
                    unique_id = '',
                    show_vid = False,
                    blind_mthd = 'easyOCR_poly_inpaint'):

#### NOTE: Seems to be dropping one frame =  last frame in empty?


    # importing the necessary libraries
    import cv2
    import numpy as np
    import os

    import easyocr
    #Doing a simple copy and past of the OCR method.  Will call later?  reader?
    #Can I pass parallel process this stuff? Or just stuff it all into a main
    #Later of course :) Because I'm going full wabi sabi!


        mask = np.zeros(img.shape[:2], dtype="uint8")
#
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
                case 'easyOCR_line_inpaint': #May remove later
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

        return img



    reader = easyocr.Reader(['en'])

    #### Change the video capture name as needed.
    vid_capture = cv2.VideoCapture(os.path.join(file_path, file_name))
    ### Onces the source of video capture is determined then start a

    if (vid_capture.isOpened() == False):
        print("Error opening video file")

    else:
        fps = vid_capture.get(5)
        frame_count = int(vid_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        print("FPS: ", fps, "/ Frame count: ", frame_count,"/ Frame width: ",  frame_width, "/ Frame height: ",frame_height)

#### Check for save folder and create if it doesn't exist

    if not os.path.isdir(os.path.join(file_path, new_path)):
        os.makedirs(os.path.join(file_path, new_path))
## Set Frame number

    frame_num = 0
#### Open video capture and run through each frame
    while(vid_capture.isOpened()):
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
        ret, frame = vid_capture.read()
        if ret == True:
            frame = blind_frame(img_src = frame, method = blind_mthd, reader=reader)
        elif:
            print("The AI module has FAILED to blind the frame.")
            exit(print(f'The video frame: {frame_num} OF {frame_count} failure'))

        #### Write the individual images
        cv2.imwrite(os.path.join(file_path, new_path,  img_prefix +  img_class +  unique_id + "frame%d.png" % frame_num), frame)
        frame_num += 1
        ### Show the video"
        if show_vid:
            cv2.imshow('original_video', frame)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
        else:
            break

    # Release the video capture object
    vid_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ocr_blind_vid()


