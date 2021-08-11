"""
This file stores functions that will analyze a
json file and retrieve custom linguistic indicators
"""


def get_total_word_count(parsed_word_frequency_data: dict) -> int:
    """
    Sums the values of the dictionary returned by parse_data()
    """
    return sum(parsed_word_frequency_data.values())


def specific_vocabulary_retrieval(parsed_word_frequency_data: dict, linguistic_indicators_list: list) -> list:
    """
    Retrieve a list of frequencies of the specified words from the word frequency data.
    The parameter category is used to subset the corpus.
    """
    meaningful_words = []
    for word in linguistic_indicators_list:
        if word not in list(parsed_word_frequency_data.keys()):
            meaningful_words.append(0)
        else:
            meaningful_words.append(parsed_word_frequency_data[word])
    return meaningful_words


def multi_criteria_extraction(parsed_word_frequency_data: dict,
                              linguistic_indicators_list: list) -> int:
    """
    Aggregates the frequencies of the words passed as an input. It is used to retrieve a global
    metric for several verb forms for instance.
    The parameter category is used to subset the corpus.
    """
    all_forms = specific_vocabulary_retrieval(parsed_word_frequency_data, linguistic_indicators_list)
    return sum(all_forms)


def get_conditional_markers(parsed_word_frequency_data: dict) -> int:
    """
    Retrieves the sum of the frequencies associated with verbs that shows marks of
    conditional (french conjugation)
    The parameter category is used to subset the corpus.
    """
    conditional_markers = []
    for word in parsed_word_frequency_data.keys():
        if word.endswith("rait") \
                or word.endswith("raient") \
                or word.endswith("riez") \
                or word.endswith("rions"):
            conditional_markers.append(parsed_word_frequency_data[word])
    return sum(conditional_markers)


def prepare_data(parsed_word_frequency_data: dict):
    """
    Functions used to retrieve the information of a custom list of
    french linguistic indicators. Returns a list of value corresponding to their
    frequency or aggregated frequency according to the function used to retrieve the information.
    :return: list of frequency
    :rtype: list
    """
    point_of_view = specific_vocabulary_retrieval(parsed_word_frequency_data,
                                                  linguistic_indicators_list=[
                                                      "je", "vous", "nous"
                                                  ])
    deliberative_words = specific_vocabulary_retrieval(parsed_word_frequency_data,
                                                       linguistic_indicators_list=["mais", "car", "donc",
                                                                                   "malgré", "pourtant",
                                                                                   "cependant"])
    adverbs = specific_vocabulary_retrieval(parsed_word_frequency_data,
                                            linguistic_indicators_list=["jamais", "toujours",
                                                                        "systématiquement", "!",
                                                                        "éventuellement"
                                                                        ])
    values = [get_total_word_count(parsed_word_frequency_data),
              multi_criteria_extraction(parsed_word_frequency_data,
                                        linguistic_indicators_list=["http", "https"]),
              multi_criteria_extraction(parsed_word_frequency_data,
                                        linguistic_indicators_list=["exemple", "exemples"]),
              multi_criteria_extraction(parsed_word_frequency_data,
                                        linguistic_indicators_list=["faut", "falloir", "faudra"]),
              multi_criteria_extraction(parsed_word_frequency_data,
                                        linguistic_indicators_list=["pouvoir", "peut", "peuvent",
                                                                    "pouvons", "pourra", "pourront",
                                                                    "pourrons"]),
              multi_criteria_extraction(parsed_word_frequency_data,
                                        linguistic_indicators_list=["devoir", "doit", "doivent",
                                                                    "devra", "devrait", "devraient",
                                                                    "devront", "devrons"]),
              get_conditional_markers(parsed_word_frequency_data)]
    values += point_of_view
    values += deliberative_words
    values += adverbs
    values.append(multi_criteria_extraction(parsed_word_frequency_data,
                                            linguistic_indicators_list=["évident", "évidemment"]))
    values.append(multi_criteria_extraction(parsed_word_frequency_data,
                                            linguistic_indicators_list=["indéniable", "indéniablement"]))
    values.append(multi_criteria_extraction(parsed_word_frequency_data,
                                            linguistic_indicators_list=["nécessaire", "nécessaires", "nécessite",
                                                                        "nécessitent",
                                                                        "nécessairement", "besoin", "besoins"]))
    return values
