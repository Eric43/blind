
def get_wordlist(wrd_list='util/rnd_word.txt')->list:
    """basic function to grab the words from rnd_wrd.txt"""
    with open(wrd_list, "r") as file:
        word_list = file.read().splitlines()

    return word_list

