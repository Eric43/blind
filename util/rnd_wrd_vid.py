def get_wordlist(wrd_list='util/rnd_word.txt')->list:
    """basic function to grab the words from rnd_wrd.txt"""
    with open(wrd_list, "r") as file:
        word_list = file.read().splitlines()

    return word_list


def rnd_wrd_vid(img,
                wrd_list: list[str], #location of filename? or just ????
                total_frames = 30,
                fps = 15,
                noise = True,
                **kwargs,):
    """give a frame or an image add a random number word in a random place
    potential kwargs are still being finished.  Basic noise class added for
    later testing of the OCR.
    """
    import numpy as np
    import cv2
    import random

    #Setting noise defaults for KWARGS et al.
    kwargs.setdefault('mean', 0.0)#Gausian
    kwargs.setdefault('std', 25.0)#Gausian
    kwargs.setdefault('noise_ratio', 0.2)#salt and pepper
    kwargs.setdefault('intensity', 25)#Random
    #noise_ratio = 0.2
    #kwargs.setdefault()
    #word_canvas.setdefault('min_x', 10)
    #May need to add a check etc.

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
            super().__init__(**kwargs)
            [self.__setattr__(key, kwargs.get(key)) for key in self.__allowed_keys_list]
            self.image = image
            #self.noise_ratio = noise_ratio

            #self.__dict__.update((key, False) for key in _allowed_keys)
            # and update the given keys by their given values
            #self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)


#Check on type provided to the different maybe Int?
        def gaussian(image: np.array, mean:float, std:float) -> np.array:
            """Gaussian noise generator given and cv2 image"""

            noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
            noisy_image = cv2.add(image, noise)

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

        def random(image:np.array, intensity:int):
            noisy_image = image.copy()
            noise = np.random.randint(-intensity, intensity + 1, noisy_image.shape)
            noisy_image = np.clip(noisy_image + noise, 0, 255).astype(np.uint8)

            return noisy_image

    # Set the video writer output
    h, w, _ = np.shape(img)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
    video_out = cv2.VideoWriter('rnd_wrds_noise_random_int20.mp4', fourcc, fps, ((w, h)))

    ####Try moving these to kwargs?
    max_x = 600
    max_y = 400
    min_x = 10
    min_y = 10

    aon = Noise #art of noise = aon

    for frame in range(total_frames):
        total_words = random.sample(wrd_list, random.randint(2,8))
        img_copy = img.copy()
        for word in total_words:
            placement = (random.randint(min_x,max_x), random.randint(min_y, max_y))
            img_copy = cv2.putText(img_copy, word, placement, cv2.FONT_HERSHEY_SIMPLEX, fontScale=random.uniform(0.25,1.5),
                              color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),thickness=3)
        if noise:
            #img_copy = aon.salt_pepper(image=img_copy, noise_ratio=kwargs.get('noise_ratio'))
            #img_copy = aon.gaussian(image=img_copy, mean= kwargs.get('mean'), std=kwargs.get('std'))
            img_copy = aon.random(image=img_copy, intensity=kwargs.get('intensity'))
        video_out.write(img_copy)

    video_out.release()
    cv2.destroyAllWindows()

    return print(f'A random word generated from {len(wrd_list)} words and contained {total_frames} total frames.')





#test_image = cv2.imread('example2_ocr_poly_inpaint.jpg')
#words = get_wordlist('util/rnd_word.txt')
#rnd_wrd_vid.rnd_wrd_vid(test_image, words)
#
