"""
This file aims to test the functions of the data_manipulation file
"""
import os
import pytest
from utils.data_manipulation import get_list_of_dict_from_categories, aggregate_several_dict, load_data

TEST_DATA_MANIP_PATH = os.path.split(os.path.realpath(__file__))[0]

INPUT_DATA = {"cat1": {"a": 1, "b": 2, "c": 3},
              "cat2": {"z": 1, "b": 2, "c": 3, "d": 4},
              "cat3": {"a": 1, "b": 2, "c": 3},
              "cat4": {"d": 1, "b": 2, "c": 3},
              "cat5": {"e": 1, "b": 2, "f": 3}}

STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(TEST_DATA_MANIP_PATH, "../test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(TEST_DATA_MANIP_PATH, "../test_data/word_frequency_test2.json")
CONFIG_1 = [(STORED_TEST_DATA_MULTI_CATEGORIES, "category 3"), (STORED_TEST_DATA_MULTI_CATEGORIES, None),
            (STORED_TEST_DATA_ONE_CATEGORY, "category 1"), (STORED_TEST_DATA_ONE_CATEGORY, None)]


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


@pytest.mark.parametrize("file_path, category", CONFIG_1)
def test_data_loading(file_path, category):
    """
    For several configuration this test checks if the function load_data() is able to
    retrieve the data normally and output the correct format.
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param category: category specified by the user
    :type category: str
    """
    final_dict = load_data(file_path, category)
    assert isinstance(final_dict, dict)
