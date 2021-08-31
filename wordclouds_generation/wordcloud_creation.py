"""
This file is responsible of wordclouds creation
"""
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def create_wordcloud_from_frequency(parsed_word_frequency_data: dict, category) -> None:
    """
    This function is used to create and save an image presenting a word-cloud based
    on a preprocessed file which will be grabbed from another docker image
    """
    word_cloud = WordCloud(background_color="white", width=1200,
                           height=600).generate_from_frequencies(parsed_word_frequency_data)
    plt.figure(figsize=(20, 10))
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    if category is not None:
        plt.savefig(os.path.join(os.getcwd(), "dist/wordcloud{}.png".format("_"+category)), bbox_inches='tight')
    else:
        plt.savefig(os.path.join(os.getcwd(), "dist/wordcloud.png"), bbox_inches='tight')
