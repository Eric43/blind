def rnd_wrd_vid(img,
                wrd_list: list[str], #location of filename? or just ????
                total_frames = 30,
                fps = 15,
                ):
    """give a frame or an image add a random number word in a random place
    potential kwargs are

    """
    import numpy as np
    import cv2
    import random

    def get_wordlist(wrd_list)->list[str]:
        """basic function to grab the words from rnd_wrd.txt"""
        with open(wrd_list, "r") as file:
            word_list = file.readlines()

        return word_list

    # Set the video writer output
    h, w, _ = np.shape(img)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec
    video_out = cv2.VideoWriter('temp_vid_name.avi', fourcc, fps, ((w, h)))
    max_x = 600
    max_y = 400
    min_x = 10
    min_y = 10
    total_words = random.sample(wrd_list, random.randint(1,4))

    for frame in range(total_frames):
        img_copy = img.copy()
        for word in total_words:
            placement = (random.randint(min_x,max_x), random.randint(min_y, max_y))
            img_copy = cv2.putText(img_copy, word, placement, cv2.FONT_HERSHEY_SIMPLEX, fontScale=random.uniform(0.1,1),
                              color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)),thickness=3)
        video_out.write(img_copy)
        """cv2.imshow('Random Word Image', img_copy)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break"""

    video_out.release()
    cv2.destroyAllWindows()

    return print(f'A random word generated from {len(wrd_list)} words and contained {total_frames} total frames.')





#test_image = cv2.imread('example2_ocr_poly_inpaint.jpg')
#words = get_wordlist('util/rnd_word.txt')
#rnd_wrd_vid.rnd_wrd_vid(test_image, words)
#
