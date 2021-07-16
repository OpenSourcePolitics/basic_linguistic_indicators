"""
This file is reponsible of wordclouds creation
"""
import os
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_wordcloud_from_frequency(file_path):
    """
    This function is used to create an image presenting a wordcloud based
    on a preprocessed file which will be grabbed from another docker image
    :param file_path: file to the json file storing the words and their associated frequency
    :type file_path: str
    """
    filename, file_extension = os.path.splitext(file_path)
    filename = os.path.basename(os.path.normpath(filename))
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    word_cloud = WordCloud(background_color="white", width=1200, height=600).generate_from_frequencies(data)
    plt.figure(figsize=(20, 10))
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(os.getcwd(), "dist/wordcloud_{}.png".format(filename)), bbox_inches='tight')
