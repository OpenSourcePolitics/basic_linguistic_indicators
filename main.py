import time
import os
from wordclouds_generation.wordcloud_creation import create_wordcloud_from_frequency
MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


if __name__ == '__main__':
    t1 = time.time()
    create_wordcloud_from_frequency(os.path.join(MAIN_PATH, "dist/word_frequency.json"))
    print(time.time()-t1)
