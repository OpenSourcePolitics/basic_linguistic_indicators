"""
This file stores functions that will analyze a
json file and retrieve custom linguistic indicators
"""
from utils.data_manipulation import load_data


def get_total_word_count(file_path, category=None):
    """
    Sums the values of the dictionary returned by load_data()
    :param file_path: path to the json file storing the data
    :type file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :return: sum of dict values
    :rtype: int
    """
    data = load_data(file_path, category)
    return sum(data.values())


def specific_vocabulary_retrieval(data_file_path, words_list, category=None):
    """
    Retrieve the values of specific words from the json data.
    The parameter category is used to subset the corpus.
    :param data_file_path: path to the json object storing the data
    :type data_file_path: str
    :param words_list: list of linguistic indicators
    :type words_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :return: list of values corresponding to the input words
    :rtype: list
    """
    meaningful_words = []
    data_file_path = load_data(data_file_path, category)
    for word in words_list:
        if word not in list(data_file_path.keys()):
            meaningful_words.append(0)
        else:
            meaningful_words.append(data_file_path[word])
    return meaningful_words


def multi_criteria_extraction(data_file_path, word_list, category=None):
    """
    Aggregates the frequencies of the words passed as an input. It is used to retrieve a global
    metric for several verb forms for instance.
    The parameter category is used to subset the corpus.
    :param data_file_path: path to the json object storing the data
    :type data_file_path: str
    :param word_list: list of linguistic indicators
    :type word_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :return: sum of the values
    :rtype: int
    """
    all_forms = specific_vocabulary_retrieval(data_file_path, word_list, category)
    return sum(all_forms)


def get_conditional_markers(data_file_path, category=None):
    """
    Retrieves the sum of the frequencies associated with verbs that shows marks of
    conditional (french conjugation)
    The parameter category is used to subset the corpus.
    :param data_file_path: path to the json object storing the data
    :type data_file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :return: sum of the values of the initial json file
    :rtype: int
    """
    conditional_markers = []
    data = load_data(data_file_path, category)
    for word in data.keys():
        if word.endswith("rait") \
                or word.endswith("raient") \
                or word.endswith("riez") \
                or word.endswith("rions"):
            conditional_markers.append(data[word])
    return sum(conditional_markers)


def prepare_data(data_file_path, category):
    """
    Functions used to retrieve the information of a custom list of
    french linguistic indicators. Returns a list of value corresponding to their
    frequency or aggregated frequency according to the function used to retrieve the information.
    :param data_file_path: path to the json object storing the data
    :type data_file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :return: list of frequency
    :rtype: list
    """
    point_of_view = specific_vocabulary_retrieval(data_file_path,
                                                  words_list=[
                                                      "je", "vous", "nous"
                                                  ],
                                                  category=category)
    deliberative_words = specific_vocabulary_retrieval(data_file_path,
                                                       words_list=["mais", "car", "donc",
                                                                   "malgré", "pourtant",
                                                                   "cependant"],
                                                       category=category)
    adverbs = specific_vocabulary_retrieval(data_file_path,
                                            words_list=["jamais", "toujours",
                                                        "systématiquement", "!",
                                                        "éventuellement"
                                                        ],
                                            category=category)
    values = [get_total_word_count(data_file_path, category),
              multi_criteria_extraction(data_file_path, word_list=["http", "https"], category=category),
              multi_criteria_extraction(data_file_path, word_list=["exemple", "exemples"], category=category),
              multi_criteria_extraction(data_file_path, word_list=["faut", "falloir", "faudra"], category=category),
              multi_criteria_extraction(data_file_path, word_list=["pouvoir", "peut", "peuvent",
                                                                   "pouvons", "pourra", "pourront",
                                                                   "pourrons"], category=category),
              multi_criteria_extraction(data_file_path, word_list=["devoir", "doit", "doivent",
                                                                   "devra", "devrait", "devraient",
                                                                   "devront", "devrons"], category=category),
              get_conditional_markers(data_file_path, category=category)]
    values += point_of_view
    values += deliberative_words
    values += adverbs
    values.append(multi_criteria_extraction(data_file_path, word_list=["évident", "évidemment"], category=category))
    values.append(multi_criteria_extraction(data_file_path, word_list=["indéniable", "indéniablement"],
                                            category=category))
    values.append(multi_criteria_extraction(data_file_path,
                                            word_list=["nécessaire", "nécessaires", "nécessite", "nécessitent",
                                                       "nécessairement", "besoin", "besoins"], category=category))
    return values
