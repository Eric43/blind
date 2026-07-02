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

def ocr_blind_vid (file_name,
                    file_path,
                    new_path = './frames',
                    img_prefix = '2v_',
                    img_class = '',
                    unique_id = '',
                    show_vid = False,
                    blind_mthd = 'AI_OCR'):

#### NOTE: Seems to be dropping one frame =  last frame in empty?


    # importing the necessary libraries
    import cv2
    import numpy as np
    import os

    import tensorflow as tf
    import keras_ocr
    ### keep here np is used for cv2 shape??

    pipeline = keras_ocr.pipeline.Pipeline()

    from blind import blind

    blind_classes = ('AI_OCR', 'block', 'both', 'sequential')

### NEED TO ADD A BLINDING OPTION CALLING THE AI BLINDING METHOD May
### need to import AI blinding option and then use in the blinding
### call.  Will need to work out the logic between top-block blind, AI
### with Black boxes and AI-OCR with bacground in painting.  Can also
### top_block, AIOCR_paint, AIOCR_block.  Can also do top_blockk
### followed by AIOCR for annotation text removal



    # Creating a VideoCapture object to read the video



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
          #### Blind the frame (if true)
          if blind_mthd in blind_classes:
              try:
                  frame = ocr_blind.ocr_blind(img_src = frame, method = blind_mthd, pipeline = pipeline)
              except:
                  print("The AI module has FAILED to blind the frame.")
                  quit()



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
    ()


