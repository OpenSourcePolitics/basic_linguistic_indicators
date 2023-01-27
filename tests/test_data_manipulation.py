"""
This file aims to test the functions of the data_manipulation file
"""
import os
import pytest
from utils.data_manipulation import get_list_of_dict_from_categories, aggregate_several_dict, parse_data
from utils.word_frequency_data_interface import LocalWordFrequencyDataLoading
from utils.system_functions import clean_directory

TEST_DATA_MANIP_PATH = os.path.split(os.path.realpath(__file__))[0]

INPUT_DATA = {"cat1": {"a": 1, "b": 2, "c": 3},
              "cat2": {"z": 1, "b": 2, "c": 3, "d": 4},
              "cat3": {"a": 1, "b": 2, "c": 3},
              "cat4": {"d": 1, "b": 2, "c": 3},
              "cat5": {"e": 1, "b": 2, "f": 3}}

STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(os.path.dirname(TEST_DATA_MANIP_PATH),
                                                 "test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(os.path.dirname(TEST_DATA_MANIP_PATH),
                                             "test_data/word_frequency_test2.json")

word_frequencies_by_cat_object_config_1 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_MULTI_CATEGORIES).load()
word_frequencies_by_cat_object_config_2 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_ONE_CATEGORY).load()

CONFIG_1 = [(word_frequencies_by_cat_object_config_1, "category 3"), (word_frequencies_by_cat_object_config_1, None),
            (word_frequencies_by_cat_object_config_2, "category 1"), (word_frequencies_by_cat_object_config_2, None)]


def test_get_list_from_dict():
    """
    This function will check if the output of get_list_of_dict_from_categories() is correct:
    [dict, dict, ..., dict]. Type check of the return and the content of the list
    """
    list_of_dicts = get_list_of_dict_from_categories(INPUT_DATA)
    check_type_sub_dict = [isinstance(elem, dict) for elem in list_of_dicts]
    assert isinstance(list_of_dicts, list) and all(check_type_sub_dict)


def test_aggregate_several_dictionaries():
    """
    this test checks that the function responsible of the merge of several dictionary
    behave normally.
    """
    validation = {'a': 2, 'c': 12, 'f': 3, 'd': 5, 'z': 1, 'e': 1, 'b': 10}
    list_of_dict = get_list_of_dict_from_categories(INPUT_DATA)
    merged_dictionary = aggregate_several_dict(list_of_dict)
    shared_items = []
    for k in list(validation.keys()):
        if validation[k] == merged_dictionary[k]:
            shared_items.append(True)
        else:
            shared_items.append(False)
    assert len(shared_items) == len(list(merged_dictionary.keys())) and all(shared_items)


@pytest.mark.parametrize("word_frequencies_by_cat_object, category", CONFIG_1)
def test_data_loading(word_frequencies_by_cat_object, category):
    """
    For several configuration this test checks if the function parse_data() is able to
    retrieve the data normally and output the correct format.
    :param word_frequencies_by_cat_object: path to the json object storing the data
    :type word_frequencies_by_cat_object:
    :param category: category specified by the user
    :type category: str
    """
    preprocessed = parse_data(word_frequencies_by_cat_object.preprocessed, category)
    classical_data = parse_data(word_frequencies_by_cat_object.unprocessed, category)
    assert isinstance(preprocessed, dict) and isinstance(classical_data, dict)


def test_clean_directory():
    """
    This test checks if the function clean_directory() is able to delete all the files
    :return:
    """
    clean_directory(os.path.join(os.path.dirname(TEST_DATA_MANIP_PATH), "dist"))
    assert len(os.listdir(os.path.join(os.path.dirname(TEST_DATA_MANIP_PATH), "dist"))) == 1
