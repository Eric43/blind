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
def ocr_blind_vid(file_name='temp_vid_name.avi',
                    file_path='/',
                    new_path = '/frames',
                    show_vid = True,
                    blind_mthd = 'easyOCR_block'):

    """Function to take a video image and blind the text (and facial?)
    Slight shift to only blinding but can add the extract frame for later use."""

#### NOTE: Seems to be dropping one frame =  last frame in empty?


    # importing the necessary libraries
    import cv2
    import numpy as np
    import os

    import easyocr
    #Doing a simple copy and past of the OCR method.  Will call later?  reader?
    #Can I pass parallel process this stuff? Or just stuff it all into a main
    #Later of course :) Because I'm going full wabi sabi!

    reader = easyocr.Reader(['en'])

    def blind_frame(img: np.array, results, method: str):
        """Basic function to take the results, image and method and blind it"""
        mask = np.zeros(img.shape[:2], dtype="uint8")
        for res in results:
            # bbox coordinates of the detected text used for legacy method
            xy = res[0]
            match method:
                case 'easyOCR_block':
                    img = cv2.fillPoly(img, pts= np.asarray([xy]), color=(0, 0, 0))
                case 'easyOCR_poly_inpaint':
                    cv2.fillPoly(mask, pts=np.asarray([xy]), color = 255)
                    # Could probably just make a mask and inpaint all at the end.
                    img = cv2.inpaint(img, mask, 2.71828, cv2.INPAINT_NS)
                case _:
                    print('The method chosen is not recognized: {blind_mthd')
                    #mayneed to return an error for the API
                    img = mask #Basically removing the img because it may contain data
                    exit()
        return img



    #### Change the video capture name as needed.
    vid_capture = cv2.VideoCapture(file_name)
    #Need to pull from the video capture?
    ### Onces the source of video capture is determined then start a

    if (vid_capture.isOpened() == False):
        print(f"Error opening video file {file_name}")

    else:
        fps = vid_capture.get(5)
        frame_count = int(vid_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        print("FPS: ", fps, "/ Frame count: ", frame_count,"/ Frame width: ",  frame_width, "/ Frame height: ",frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec
    video_out = cv2.VideoWriter('temp_vid_name.avi', fourcc, fps, (frame_width, frame_height))
#### Check for save folder and create if it doesn't exist

    """if not os.path.isdir(new_path):
        os.makedirs(new_path)
## Set Frame number"""

    frame_num = 0
#### Open video capture and run through each frame
    while(vid_capture.isOpened()):
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
        ret, frame = vid_capture.read()
        if ret == True:

            results = reader.readtext(frame,
                          text_threshold=0.5,
                          low_text=0.25,
                          min_size=6,
                          )
            if len(results) > 0:
                frame = blind_frame(img=frame, results=results, method=blind_mthd)
            video_out.write(frame)
        elif ret!=True:
            print("The AI module has FAILED to blind the frame.")
            exit(print(f'The video frame: {frame_num} OF {frame_count} failure'))

        #### Write the individual images
        #cv2.imwrite(os.path.join(file_path, new_path,  img_prefix +  img_class +  unique_id + "frame%d.png" % frame_num), frame)
        #frame_num += 1
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
    video_out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ocr_blind_vid()


