"""
This file stores functions that will analyze a
json file and retrieve custom linguistic indicators
"""
import json


def retrieve_data(data_file_path):
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data_file_path = json.load(f)
    return data_file_path


def get_total_word_count(data_file_path):
    data = retrieve_data(data_file_path)
    return sum(data.values())


def specific_vocabulary_retrieval(data_file_path, words_list):
    meaningful_words = []
    data_file_path = retrieve_data(data_file_path)
    for word in words_list:
        if word not in list(data_file_path.keys()):
            meaningful_words.append(0)
        else:
            meaningful_words.append(data_file_path[word])
    return meaningful_words


def multi_criteria_extraction(data_file_path, word_list):
    all_forms = specific_vocabulary_retrieval(data_file_path, word_list)
    return sum(all_forms)


def get_conditional_markers(data_file_path):
    conditional_markers = []
    data = retrieve_data(data_file_path)
    for word in data.keys():
        if word.endswith("rait") \
                or word.endswith("raient") \
                or word.endswith("riez") \
                or word.endswith("rions"):
            conditional_markers.append(data[word])
    return sum(conditional_markers)


def prepare_data(data_file_path):
    point_of_view = specific_vocabulary_retrieval(data_file_path,
                                                  words_list=[
                                                      "je", "vous", "nous",
                                                  ])
    deliberative_words = specific_vocabulary_retrieval(data_file_path,
                                                       words_list=["mais", "car", "donc",
                                                                   "malgré", "pourtant",
                                                                   "cependant"])
    adverbs = specific_vocabulary_retrieval(data_file_path,
                                            words_list=["jamais", "toujours",
                                                        "systématiquement", "!",
                                                        "éventuellement"
                                                        ])
    values = [get_total_word_count(data_file_path),
              multi_criteria_extraction(data_file_path, word_list=["http", "https"]),
              multi_criteria_extraction(data_file_path, word_list=["exemple", "exemples"]),
              multi_criteria_extraction(data_file_path, word_list=["faut", "falloir", "faudra"]),
              multi_criteria_extraction(data_file_path, word_list=["pouvoir", "peut", "peuvent",
                                                                   "pouvons", "pourra", "pourront",
                                                                   "pourrons"]),
              multi_criteria_extraction(data_file_path, word_list=["devoir", "doit", "doivent",
                                                                   "devra", "devrait", "devraient",
                                                                   "devront", "devrons"]),
              get_conditional_markers(data_file_path)]
    values += point_of_view
    values += deliberative_words
    values += adverbs
    values.append(multi_criteria_extraction(data_file_path, word_list=["évident", "évidemment"]))
    values.append(multi_criteria_extraction(data_file_path, word_list=["indéniable", "indéniablement"]))
    values.append(multi_criteria_extraction(data_file_path,
                                            word_list=["nécessaire", "nécessaires", "nécessite", "nécessitent",
                                                       "nécessairement", "besoin", "besoins"]))
    return values
