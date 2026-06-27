########################################
####  blind ultra sound function   #####
#### Designed to work with images     ##
### and then send to the selected   ####
## blinding method(s).  Can be batched #
### 2024 ewo Licensed GPLv3            #
########################################


def blind(img_src, ##image -or- FOLDER IF BATCH = True
          classification = None, #file name prefix more descriptive
          method = 'AI_OCR',
          img_type = '.jpg', ### EXPAND TO JPG, JPEG and PNG?
          save_path = "./Blind",
          batch = False,
          auto_size = True, #Applies to header block only
          AI_bkgnd = "inpaint",
          i = 0,
          block = dict([("xmin" , 0),
                        ("ymin" , 0),
                        ("xmax" , 960),
                        ("ymax" , 60)]),
          dir_label = ["block", "AI_OCR"],
          log_save = False, #TODO?Maybe? NEVER the orginal name for HIPAA
          debug = False):

    """blind() function designed to be used in the blinding of
    medical images through the use of multiple methods from simple
    header block to character recognition and removal or both.

    args:

    img_src: this is either the image location or a folder
    containing images

    kwargs:

    classification: default = None and is designed to add an image
    classifier prefix

    method: default = AI_OCR using Keras ocr.  Options are "AI_OCR",
    "sequential", "block", or "both"

    img_type: default = 'jpg'

    save_path: The folder where the blinded images will be saved.
    Default = './Blind'

    batch: default = False.  When set to True and provided a folder in
    img_src it will blind all the images in the folder.  TODO: Extract
    name from folder?

    auto_size: default = True. This is used for the block header
    method and adjust header bar size as a function of image size.

    AI_bkgnd: default = 'inpaint' this takes the background and
    inpaints the text bounding box.  Option is 'black' for a bar
    accross the text.

    i: this is the image number can be set to 0 or any N to aid in
    keeping images and image frames from video extraction seperate.

    block:  dict with the header block size standard.

    dir_label: if there are more than one time of blinding
    [sequential] it will default to these dir names.

    log_save:  to create a use log in todo state.

    debug: default = false this adds print statements when debugging
    the orginal version.

    """

### add auto-size for setting header block H size based on img size.

#### Will develop an *.org file for TODO lists etc.
#Need to add recursive folder serach or  fa seperate batch function.

#### slowly reformatting to a stand alone fx instead of a jupyter
#### notebook entry

############################################################################
#                         Packages
# Written ewo June 2024
# Edited last ewo 25jul2024 ~ Modified TF session init for mem growthy
# Editied May 2025 to work with tensorflow-mac py 3.10 and tf 2.14.1
############################################################################

    #Packages (May move to individual functions...????).  Just doing this
#to work in my conda TF env. with current default settings.

    import os
    import datetime
    import cv2
    import math
    import numpy as np
    import keras_ocr
    ### keep here np is used for cv2 shape??

    pipeline = keras_ocr.pipeline.Pipeline()

### Initialize TF???? #### IFF used by the function.
    #if method != "block":
        ### May need to add a check for TF and install CPU or GPU boolean

        #import tensorflow as tf

        #### NEED TO TRY V2?  Or diffferent method of memory allocation?
        #config = tf.compat.v1.ConfigProto()
        #config.gpu_options.allow_growth = True #### Still mem errors? Keras-ocr session?
        #session = tf.compat.v1.Session(config=config)

        #import keras_ocr ### NOTE Keras can also config mem allocation size!  Try this!

        ### NOTE: Keras_ocr did not work with tf >2.15.* had to
        ### "downgrade" from 2.17.*

############################################################################
#                         Required functions
# Written ewo June 2024
# 26July2024 Img color flipped on save.  Added cvtColor
############################################################################
## General block blinding header information.  This is used in block,
## sequential and both.  This will then be either saved or AI_OCR.

    def block_blind (img_src,
                     auto_size,
                     xmin = block['xmin'], ##May change the dictionary
                     xmax = block['xmax'],
                     ymin = block['ymin'],
                     ymax = block['ymax']): # header block = ~8.4% y max


        if debug : print("block fx.")

        # read img
        try:
            img = cv2.imread(img_src, cv2.IMREAD_COLOR)
        except:
            print('Image:', img_src, ' not loaded!')
            quit()
        #### Check the image.  Seems to be "reversed" after save
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # set block header size (good for varied img sizes)
        if auto_size :
            if debug : print(img.shape)
            h, w, _ = img.shape
            xmin = 0
            ymin = 0
            xmax = w
            ymax = round(0.084 * h)

        #####Determine the image size and adjust width and height????
        return (cv2.rectangle(img, (xmin,ymin), (xmax, ymax), (0,0,0), -1))
    #### NOT ALL ARE 640x480 autosize can adjust block height.
    ############################################################################

    ############################################################################
    # AI OCR functions follow:
    ############################################################################
    #####NEXT SEVERAL FUNCTIONS USED IN AI OCR (need link)
    ## The initial work for keras-ocr

    def AI_OCR(img_src,
               AI_bkgnd, pipeline):

        if debug : print("AI_OCR fx")
        #

        #maybe move the midpoint fx here?
        def midpoint(x1, y1, x2, y2):
            x_mid = int((x1 + x2)/2)
            y_mid = int((y1 + y2)/2)
            return (x_mid, y_mid)

        # read image
        try:
            img = keras_ocr.tools.read(img_src)
        except:
            print('unable to read image - quiting processing ')
            quit()

        # generate (word, box) tuples
        prediction_groups = pipeline.recognize([img])
        mask = np.zeros(img.shape[:2], dtype="uint8")
        for box in prediction_groups[0]:
            x0, y0 = box[1][0]
            x1, y1 = box[1][1]
            x2, y2 = box[1][2]
            x3, y3 = box[1][3]

            if AI_bkgnd == "inpaint":

                x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
                x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)

                thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))

            ## Using openCV to inpaint the identified text
                cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255,
                thickness)
                img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

            elif AI_bkgnd == "black":
                cv2.rectangle(img, (int(x0), int(y0)), (int(x1), int(y3)), (0, 0, 0), -1)

        return(img)

    ########################################################################
    #####  Saving the image
    ########################################################################

    def save_img(img,
                 save_path,
                 classification, #prefix?
                 log_save = False):

        if debug : print("save_img fx")
        #Check for the new folder and if not there then add:

        ###  I don't know about string (loop iteration number).  This
        ###  should be added to header information that can be passed
        ###  in the classification?
        timestamp = str(datetime.datetime.now().strftime("_%Y%m%d|%H:%M:%S"))
        new_name = classification + timestamp + '.jpg'
        if debug : print(new_name)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            cv2.imwrite(os.path.join(save_path, new_name), img_rgb)
        except:
            print('Image:  ', new_name, ' not saved!')
            quit()
        return(print("File saved: ", new_name))




    ########################################################################
    # Run the correct blinding method.
    # This was modified from a stand alone blind method to include batch.
    #######################################################################

    def blind_type(method,
                   img_src,
                   auto_size,
                   save_path,
                   classification,
                   AI_bkgnd,
                   block,
                   dir_label,
                   log_save):


        if method == "block":
            print("Block method selected")
            temp = block_blind(img_src, auto_size)
            save_img(temp, save_path, classification, log_save)
        elif method == "AI_OCR":
            print("AI_OCR with " + AI_bkgnd + " selected.")
            temp = AI_OCR(img_src, AI_bkgnd, pipeline)
            save_img(temp, save_path, classification, log_save)
        elif method == "sequential":
            temp = block_blind(img_src, auto_size)
            temp = AI_OCR(temp, AI_bkgnd, pipeline) #TF unhappy switch order?
            save_img(temp, save_path, classification, log_save)
        elif method == "both":
            #Block blind first
            temp = block_blind(img_src, auto_size)
            save_img(temp, os.path.join(save_path, dir_label[0]), classification, log_save)
            #Same unaltered image run through AI OCR
            temp = AI_OCR(img_src, AI_bkgnd, pipeline)
            save_img(temp, os.path.join(save_path, dir_label[1]), classification, log_save)
        else:
            print ("method not correctly selected")



    ########################################################################
    # BATCH BLINDING FUNCTIONS FOLLOW
    #
    #
    #
    ########################################################################


############################################################################
#                         Required functions for blinding
# Written ewo June 2024 as one "big a$$" function from disparate notebooks
# 26July2024 combined with us_blind to make blind.py
# 26July2024 Wrote main, broke out functions.
# 26July2024 Img color flipped on save for block blind.  Added cvtColor
############################################################################

# Define file list turn into a function
    def get_files (path, img_type):
        if debug : print("get_files")

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(img_type):
                    file_list.append(os.path.join(root, file))

        return(file_list)
#Need to use a file list when tried concurrently it kept
#recurssively looping.

############################################################################
    ### loop through file list and call us_blind fx
    def blind_flist (file_list,
                     i,
                     img_class,
                     method):
        if debug : print("blind fx")
        for f in file_list:
            classification = '_'.join([img_class, str(i)])
            blind_type(method, str(f),auto_size, save_path, classification, AI_bkgnd, block, dir_label, log_save) ### CHANGE CALL TO US_BLIND
            i = i + 1

############################################################################
#                         MAIN Program
############################################################################
# Written ewo May-June 2024 with main being slowly added as function move.
# Derived from multiple overlapping jupyter notebook with min fx's.
# Edits:
# 25July2024 Added blinding block auto sizing
# 24July2024 TF issues.  Random memory errors ~dynamic memory w/ grow.
# Initial allocation (~5.95 gb?) is too large for the 1070ti. Set a fix %?
# Early July Clean up code and document.  FIX TF INSTALL! (2.17 n/a ocr)
#
# TODO:  Keras-ocr seems to use depreciated resizing code.
#        Need to see if its too difficult to modify.

#### UPDATE: Keras-ocr on github and one of the old resize calls
#### depreciated.  Maybe fork, fix and push?
############################################################################

    if __name__ == "__main__":

        if debug :
            print("main (debug) classification set to debug_")
            classification = "debug_"

        if not os.path.isdir(save_path):
            print("Save path folder not present one is being created at", save_path)
            os.makedirs(save_path)
        if method == "both" and not (os.path.isdir(os.path.join(save_path, "AI_OCR"))):
            for f in dir_label:
                os.makedirs(os.path.join(save_path, f))

        #Check for the destination directory of the blinded images:
        #ck_dirs(save_path)
        #Check if its one or batch? can os.walk handle a onesy?
        if not batch:
            if debug : print("One-at-a-time")
            blind_type(method=method,
                       img_src=img_src,
                       auto_size=auto_size,
                       save_path=save_path,
                       classification=classification,
                       AI_bkgnd=AI_bkgnd,
                       block=block,
                       dir_label=dir_label,
                       log_save=log_save)#lots of stuff)
        elif batch:
            if debug : print("batch method")
            file_list = []
            path = os.path.normpath(img_src) # move to fx?
            file_list = get_files(path, img_type)
            blind_flist(file_list, i, classification, method)



### end us_blind.py working on tf 2.15.0 on 23july 2024 ewo

#if batch = true

############################################################################

###NOTES:
#Not sure of the use of dictionary for cropping size. Wanted to
#automate the process based upon image size. i.e. If a 640x480 then use
#these min/max for block blinding.

# TODO: It seems that keras-ocr is not doing the correct resizing
# calls and other issues with current tf or nightly.  Need to see how
# hard it is to correct?

#potential ways to clear
#gpu memory import tensorflow as tf tf.keras.backend.clear_session()

# Need to add an exit session for the end?

### Testing:
### 26July2024 Tested two different .jpg files in all
### blinding methods.  It worked.  TF init still slow and initial
### memory allocation error but it works.  Needed the cvt color added
### in block blind.


### NOTE: Going to have to move the block blinding part into the
### us_blind method.  Only one TF init.



#
