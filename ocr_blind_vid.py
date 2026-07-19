
#### Working on for pytorch conversion.
def ocr_blind_vid(file_name='rnd_wrds_1.mp4',
                    file_path='/',
                    new_path = '/frames',
                    show_vid = False,
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

    def blind_frame(img, results, method: str):
        """Basic function to take the results, image and method and blind it"""
        mask = np.zeros(img.shape[:2], dtype="uint8")

        for res in results:
            # bbox coordinates of the detected text used for legacy method
            xy = res[0]
            match method:
                case 'easyOCR_block':
                    print(f'xy = {[xy]}')
                    img = cv2.fillPoly(img, pts= np.asarray([xy], dtype = np.int32), color=(0, 0, 0))

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
        quit()


    fps = vid_capture.get(5)
    frame_count = int(vid_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))

    print("FPS: ", fps, "/ Frame count: ", frame_count,"/ Frame width: ",  frame_width, "/ Frame height: ",frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
    video_out = cv2.VideoWriter('temp_vid_name.mp4', fourcc, fps, (frame_width, frame_height))

    frame_num = 0
#### Open video capture and run through each frame
    while(vid_capture.isOpened()):
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
        ret, frame = vid_capture.read()
        if ret != True:
            #note move to error or exception type call ?
            break
        results = reader.readtext(frame,
                        text_threshold=0.5,
                        low_text=0.25,
                        min_size=6,
                        )
        print(f'The OCR found {len(results)} text boxes in frame {frame_num}.')
        if len(results) > 0:
            frame = blind_frame(img=frame, results=results, method=blind_mthd)

        video_out.write(frame)

        #### Write the individual images
        #cv2.imwrite(os.path.join(file_path, new_path,  img_prefix +  img_class +  unique_id + "frame%d.png" % frame_num), frame)
        #frame_num += 1
        ### Show the video"
        frame_num += 1


    # Release the video capture object
    vid_capture.release()
    video_out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ocr_blind_vid()


