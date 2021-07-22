"""
Stores data manipulation functions
"""
import json


def get_list_of_dict_from_categories(initial_dict):
    """
    Creates a list of dictionaries. Each one stores the words and their frequency
    by category
    :param initial_dict: dictionary object where the keys are the categories contained in
    the dataset and the values are a dictionary storing the words and their frequency.
    :type initial_dict: dict
    :return: list of frequency dictionary
    :rtype: list
    """
    dictionary_by_category = [count for _, count in initial_dict.items()]
    return dictionary_by_category


def merge_two_dictionaries(dict_1, dict_2):
    """
    Merge two dictionaries on their keys and sum their values
    :param dict_1: first dictionary
    :type dict_1: dict
    :param dict_2: second dictionary
    :type dict_2: dict
    :return: single dictionary based on the former ones (the unique keys of each source dict
    are kept in the output)
    :rtype: dict
    """
    merged_dict = {}
    for k in set(dict_1) | set(dict_2):
        merged_dict[k] = dict_1.get(k, 0) + dict_2.get(k, 0)
    return merged_dict


def aggregate_several_dict(list_of_dict):
    """
    For a list of several dictionaries this function will merge them all
    two by two on their keys by summing their values.
    A key present in dict 1 but not in dict 2 will be kept in the output..
    :param list_of_dict: list of dictionary to be merged
    :type list_of_dict: list
    :return: merged dictionary storing all the information
    :rtype: dict
    """
    while len(list_of_dict) > 2:
        merged_dict = merge_two_dictionaries(list_of_dict[0], list_of_dict[1])
        list_of_dict = [merged_dict] + list_of_dict[2:]
        aggregate_several_dict(list_of_dict)
    final_merged_dict = merge_two_dictionaries(list_of_dict[0], list_of_dict[1])
    return final_merged_dict


def load_data(file_path, category=None):
    """
    From a json object this function will load the data that will be used in
    textual data valuation functions.
    :param file_path: path to the json file (retrieved from nlp_preprocessing project)
    :type file_path: str
    :param category: category specified by the user that subset the global data
    :return:dictionary object storing all the vocabulary and its frequency if category is None.
    Otherwise it will store only the vocabulary of a specific category
    :rtype: dict
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if category is None:
        if len(list(data.keys())) > 1:
            list_of_dictionaries = get_list_of_dict_from_categories(data)
            final_dictionary = aggregate_several_dict(list_of_dictionaries)
        else:
            final_dictionary = data[list(data.keys())[0]]
    else:
        final_dictionary = data[category]
    return final_dictionary
