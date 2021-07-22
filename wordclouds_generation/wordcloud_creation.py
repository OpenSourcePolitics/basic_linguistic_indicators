"""
This file is responsible of wordclouds creation
"""
import os
from operator import itemgetter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.data_manipulation import load_data


def get_most_common_words(file_path, category=None, number_of_words=50):
    """
    This function will return the most common words
    :param file_path:
    :param category:
    :param number_of_words: number of most common words
    :return: list of most common words in the corpus
    :rtype: list
    """
    data = load_data(file_path, category)
    sorted_data = sorted(data.items(), key=itemgetter(1), reverse=True)
    return sorted_data[:number_of_words]


def create_wordcloud_from_frequency(file_path, category=None):
    """
    This function is used to create an image presenting a wordcloud based
    on a preprocessed file which will be grabbed from another docker image
    :param file_path: file to the json file storing the words and their associated frequency
    :type file_path: str
    :param category: name of the category to study
    """
    filename, _ = os.path.splitext(file_path)
    filename = os.path.basename(os.path.normpath(filename))
    data = load_data(file_path, category)
    word_cloud = WordCloud(background_color="white", width=1200, height=600).generate_from_frequencies(data)
    plt.figure(figsize=(20, 10))
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(os.getcwd(), "dist/wordcloud_{}.png".format(filename)), bbox_inches='tight')
