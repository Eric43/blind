""""
Collection of stuff used to generate random word videos and images for testing


Very Basic use:
#test_image = cv2.imread('example2_ocr_poly_inpaint.jpg')
#words = get_wordlist('util/rnd_word.txt')
#rnd_wrd_vid(test_image, words)
Will generate a video (15fps and 30 frames default)

Creating a test img dataset with random words:

"""

import os
import random
import uuid  #Use later just to assign a filename.

import cv2
import numpy as np
from tqdm import tqdm


class Noise:
    """
        Basic class to add noise to a image (np.array)
        Three classes of noise: Gausian, Salt and Pepper and Random
        Initial functions are from the site:
        https://www.askpython.com/python/examples/adding-noise-images-opencv

        image is np.array
        noise_ratio = 0.2 #Salt and pepper
        image is a opencv np.array

        **Kwargs
        #Gaussian noise
        mean (default = 0)
        std (default = 25)
        #Salt and Pepper
        noise_ratio (INOP currently in the initial call)
        #Random
        intensity (default = 25)
    """


    _allowed_keys = ['mean','sd','noise_ratio', 'intensity']
    def __init__ (self, image: np.array, **kwargs):
        kwargs.setdefault('mean', 0.0)#Gausian
        kwargs.setdefault('std', 25.0)#Gausian
        kwargs.setdefault('noise_ratio', 0.2)#salt and pepper
        kwargs.setdefault('intensity', 25)#Random
        #Setting the text canvas size
        kwargs.setdefault('max_x', 600)
        kwargs.setdefault('max_y', 400)
        kwargs.setdefault('min_x', 10)
        kwargs.setdefault('min_y', 10)

        super().__init__(**kwargs)
        [self.__setattr__(key, kwargs.get(key)) for key in self.__allowed_keys_list]
        self.image = image

    def gaussian(image: np.array, mean:float, std:float) -> np.array:
        """Gaussian noise generator given and cv2 image"""
        img_copy = image.copy()
        noise = np.random.normal(mean, std, img_copy.shape).astype(np.uint8)
        noisy_image = cv2.add(img_copy, noise)

        return noisy_image

    def salt_pepper(image: np.array, noise_ratio:float) -> np.array:
        """basic salt and pepper noise for cv2 images."""
        noisy_image = image.copy()
        h, w, c = noisy_image.shape
        noisy_pixels = int(h * w * noise_ratio)

        for _ in range(noisy_pixels):
            row, col = np.random.randint(0, h), np.random.randint(0, w)
            if np.random.rand() < 0.5:
                noisy_image[row, col] = [0, 0, 0]
            else:
                noisy_image[row, col] = [255, 255, 255]

        return noisy_image

    def random(image:np.array, intensity:int) -> np.array:
        noisy_image = image.copy()
        noise = np.random.randint(-intensity, intensity + 1, noisy_image.shape)
        noisy_image = np.clip(noisy_image + noise, 0, 255).astype(np.uint8)

        return noisy_image


def get_wordlist(wrd_list='util/rnd_word.txt')->list:
    """basic function to grab the words from rnd_wrd.txt"""
    with open(wrd_list, "r") as file:
        word_list = file.read().splitlines()

    return word_list

def rnd_wrd_img(*img : list, wrd_list: list[str], noise, **kwargs):
    """Given one or more images add random amount of random placed text."""
      #Setting noise defaults for KWARGS et al.
    kwargs.setdefault('mean', 0.0)#Gausian
    kwargs.setdefault('std', 25.0)#Gausian
    kwargs.setdefault('noise_ratio', 0.2)#salt and pepper
    kwargs.setdefault('intensity', 25)#Random
    #Setting the text canvas size
    kwargs.setdefault('max_x', 600)
    kwargs.setdefault('max_y', 400)
    kwargs.setdefault('min_x', 10)
    kwargs.setdefault('min_y', 10)
    #Set kwargs for changing text?
    max_x = kwargs.get('max_x')
    max_y = kwargs.get('max_y')
    min_x = kwargs.get('min_x')
    min_y = kwargs.get('min_y')

    aon = Noise

    for i in tqdm(img):
        total_words = random.sample(wrd_list, random.randint(2,8))
        img_copy = cv2.imread(filename=i)
        for word in total_words:
            placement = (random.randint(min_x,max_x), random.randint(min_y, max_y))
            img_copy = cv2.putText(img_copy, word, placement, cv2.FONT_HERSHEY_SIMPLEX, fontScale=random.uniform(1,1.5),
                              color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),thickness=1)
        if noise:
            #Note:  Need to figure out how I want to call this.
            img_copy = aon.salt_pepper(image=img_copy, noise_ratio=kwargs.get('noise_ratio'))
            #img_copy = aon.gaussian(image=img_copy, mean= kwargs.get('mean'), std=kwargs.get('std'))
            #img_copy = aon.random(image=img_copy, intensity=kwargs.get('intensity'))
        cv2.write(img, filename= uuid)

    return print ('Random images created and saved')



def rnd_wrd_vid(img,
                wrd_list: list[str], #location of filename? or just ????
                total_frames = 30,
                fps = 15,
                noise = True,
                **kwargs,):
    """give a frame or an image add a random number word in a random place
    potential kwargs are still being finished.  Basic noise class added for
    later testing of the OCR.

    **kwargs:
    Noise class:
    1.  Gaussian noise
    mean, 0
    std, 25
    2.  Salt and Pepper Noise
    noise_ratio, 0.2
    3.  Random Noise
    intensity, 25
    Text placement:
    4. Text Canvas size
    max_x
    max_y
    min_x
    min_y

    """

    #Check if kwargs are submitted and "acceptable" if not pop and error?
    #Setting noise defaults for KWARGS et al.
    kwargs.setdefault('mean', 0.0)#Gausian
    kwargs.setdefault('std', 25.0)#Gausian
    kwargs.setdefault('noise_ratio', 0.2)#salt and pepper
    kwargs.setdefault('intensity', 25)#Random
    #Setting the text canvas size
    kwargs.setdefault('max_x', 600)
    kwargs.setdefault('max_y', 400)
    kwargs.setdefault('min_x', 10)
    kwargs.setdefault('min_y', 10)
    #Set kwargs for changing text?



    # Set the video writer output
    h, w, _ = np.shape(img)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
    video_out = cv2.VideoWriter('rnd_wrds_noise_random_int20.mp4', fourcc, fps, ((w, h)))

    ####Try "automating"
    max_x = kwargs.get('max_x')
    max_y = kwargs.get('max_y')
    min_x = kwargs.get('min_x')
    min_y = kwargs.get('min_y')

    aon = Noise #art of noise = aon

    for frame in tqdm(range(total_frames)): #Use frame count later for N_rnd_wrds
        total_words = random.sample(wrd_list, random.randint(2,8))
        img_copy = img.copy()
        for word in total_words:
            placement = (random.randint(min_x,max_x), random.randint(min_y, max_y))
            img_copy = cv2.putText(img_copy, word, placement, cv2.FONT_HERSHEY_SIMPLEX, fontScale=random.uniform(1,1.5),
                              color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),thickness=2)
        if noise:
            #Note:  Need to figure out how I want to call this.
            #img_copy = aon.salt_pepper(image=img_copy, noise_ratio=kwargs.get('noise_ratio'))
            #img_copy = aon.gaussian(image=img_copy, mean= kwargs.get('mean'), std=kwargs.get('std'))
            img_copy = aon.random(image=img_copy, intensity=kwargs.get('intensity'))
        video_out.write(img_copy)

    video_out.release()
    cv2.destroyAllWindows()

    return print(f'A random word generated from {len(wrd_list)} words and contained {total_frames} total frames.')

def load_cv_img(file_name):
    """Basic load in util for now need to add a check later."""
    img = cv2.imread(filename=file_name)

    return img

def get_directory_contents(folder_location:str):
        """General support function to get folder contents and full path."""
        img_ext = ['.png', '.jpg',]
        #vid_ext = ['mp4', 'avi',]
        directory_path = folder_location
        files = []

        try:
            for entry in os.listdir(directory_path):
                if entry.endswith(tuple(img_ext)) and os.path.isfile(os.path.join(directory_path, entry)):
                    files.append(os.path.join(directory_path,entry))
        except FileNotFoundError:
            print(f"The directory {directory_path} does not exist.")
        except PermissionError:
            print(f"Permission denied to access {directory_path}.")
        return files

def create_std_test_set(folder_location, word_mask:np.array, noisy_data= True, noise_max=10, **kwargs):
        """Basic util to create a series standard text images on different image background
        with a range of noise types and amounts."""
        ###I need to move these uptop and set a DICT.?
        #Setting noise defaults for KWARGS et al.
        kwargs.setdefault('mean', 0.0)#Gausian
        kwargs.setdefault('std', 25.0)#Gausian
        kwargs.setdefault('noise_ratio', 0.2)#salt and pepper
        kwargs.setdefault('intensity', 25)#Random
        kwargs.setdefault('save_location', 'rnd_test_imgs/')
        #Setting the text canvas size
        kwargs.setdefault('max_x', 600)
        kwargs.setdefault('max_y', 400)
        kwargs.setdefault('min_x', 10)
        kwargs.setdefault('min_y', 10)
        kwargs.setdefault('img_type', '.png')

        aon = Noise
        alpha = 0.5  # Transparency factor

        files= get_directory_contents(folder_location=folder_location)
        print(files)

        for file in tqdm(files):
            unique_id = str(uuid.uuid4().hex)
            new_name = (os.path.join(kwargs.get('save_location'), unique_id + kwargs.get('img_type')))
            print(new_name)
            # Blend the original image and the overlay
            img = cv2.imread(file)
            blended_image = cv2.addWeighted(img, 1 - alpha, word_mask, alpha, 0)
            img_copy = blended_image.copy()
            if not noisy_data and not cv2.imwrite(os.path.join(kwargs.get('save_location'), unique_id + kwargs.get('img_type')), blended_image):
                    raise OSError("Could not write image")
            if noisy_data:
                for noise_amount in range(noise_max):
                    saltimg = aon.salt_pepper(image=img_copy, noise_ratio= noise_amount*.1 )
                    if not (cv2.imwrite(os.path.join(kwargs.get('save_location'),str(noise_amount)+'_salt_pepper_'+unique_id+ '.png' ), saltimg)):
                        raise OSError("Could not write the salt and pepper image!")
                    gaussimg = aon.gaussian(image=img_copy, mean=0, std=noise_amount*.5)
                    if not (cv2.imwrite(os.path.join(kwargs.get('save_location'), str(noise_amount)+'_gaussian_'+unique_id+'.png' ), gaussimg)):
                        raise OSError("Couldn't save the gaussian noise image!")

        return print(f'A standardized text, different background set was saved to {kwargs.get('save_location')}')
