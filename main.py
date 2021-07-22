import time
import os
from wordclouds_generation.wordcloud_creation import create_wordcloud_from_frequency, get_most_common_words
MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


if __name__ == '__main__':
    t1 = time.time()
    get_most_common_words(file_path=os.path.join(MAIN_PATH, "dist/word_frequency_test_preprocessed.json"))
    create_wordcloud_from_frequency(os.path.join(MAIN_PATH, "dist/word_frequency_subset_raw_data_preprocessed.json"))
    print(time.time()-t1)
