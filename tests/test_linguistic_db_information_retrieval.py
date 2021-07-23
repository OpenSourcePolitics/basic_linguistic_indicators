"""
This file is checks that the information retrieval process is working correctly
"""
import os
import pytest
from linguistic_database.ldb_information_retrieval import get_total_word_count, specific_vocabulary_retrieval, \
    multi_criteria_extraction, get_conditional_markers, prepare_data

TEST_LDB_IR = os.path.split(os.path.realpath(__file__))[0]
STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(TEST_LDB_IR, "../test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(TEST_LDB_IR, "../test_data/word_frequency_test2.json")

CONFIG_SUM = [(STORED_TEST_DATA_MULTI_CATEGORIES, "category 3", 63), (STORED_TEST_DATA_MULTI_CATEGORIES, None, 321),
              (STORED_TEST_DATA_ONE_CATEGORY, "category 1", 218), (STORED_TEST_DATA_ONE_CATEGORY, None, 218)]

CONFIG_WORD_RETRIEVAL = [(STORED_TEST_DATA_MULTI_CATEGORIES, ["word1", "word2", "not_in_list"],
                          "category 3", [5, 20, 0]),
                         (STORED_TEST_DATA_MULTI_CATEGORIES, ["word1", "word2", "not_in_list"], None, [95, 31, 0]),
                         (STORED_TEST_DATA_ONE_CATEGORY, ["word1", "word2", "not_in_list"], "category 1", [1, 5, 0]),
                         (STORED_TEST_DATA_ONE_CATEGORY, ["word1", "word2", "not_in_list"], None, [1, 5, 0])]

CONFIG_CONDITIONAL_MARKERS = [(STORED_TEST_DATA_MULTI_CATEGORIES, "category 2", 30),
                              (STORED_TEST_DATA_MULTI_CATEGORIES, None, 30),
                              (STORED_TEST_DATA_ONE_CATEGORY, "category 1", 95),
                              (STORED_TEST_DATA_ONE_CATEGORY, None, 95)]

CONFIG_DATA_PREPARATION = [(STORED_TEST_DATA_MULTI_CATEGORIES, "category 2"),
                            (STORED_TEST_DATA_MULTI_CATEGORIES, None),
                            (STORED_TEST_DATA_ONE_CATEGORY, "category 1"),
                            (STORED_TEST_DATA_ONE_CATEGORY, None)]


@pytest.mark.parametrize("file_path, category, output", CONFIG_SUM)
def test_get_total_count(file_path, category, output):
    """
    Checks that the sum of the values is correct
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: int
    """
    dict_sum = get_total_word_count(file_path, category)
    assert isinstance(dict_sum, int) and dict_sum == output


@pytest.mark.parametrize("file_path, word_list, category, output", CONFIG_WORD_RETRIEVAL)
def test_specific_word_retrieval(file_path, word_list, category, output):
    """
    Checks that specific_word_retrieval works properly :
        - retrieve the values of the words specified as inputs
        - appends 0 if the words is not in the data
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param word_list: list of linguistic indicators
    :type word_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    words_frequency = specific_vocabulary_retrieval(file_path, word_list, category)
    assert isinstance(words_frequency, list) and words_frequency == output


@pytest.mark.parametrize("file_path, word_list, category, output", CONFIG_WORD_RETRIEVAL)
def test_multi_criteria_extraction(file_path, word_list, category, output):
    """
     Checks that multi_criteria_extraction works properly :
        - output a single metric for the initial words
        - correct type
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param word_list: list of linguistic indicators
    :type word_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    indicators_frequency = multi_criteria_extraction(file_path, word_list, category)
    assert isinstance(indicators_frequency, int) and indicators_frequency == sum(output)


@pytest.mark.parametrize("file_path, category, output", CONFIG_CONDITIONAL_MARKERS)
def test_conditional_markers_retrieval(file_path, category, output):
    """
    Checks that the conditional markers retrieval works properly
        - correct output
        - correct type
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    conditional_markers_frequency = get_conditional_markers(file_path, category)
    assert isinstance(conditional_markers_frequency, int) and conditional_markers_frequency == output


@pytest.mark.parametrize("file_path, category", CONFIG_DATA_PREPARATION)
def test_data_preparation(file_path, category):
    """
    Checks the behavior of the data preparation function
        - correct number of values
        - correct type
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    """
    indicators = prepare_data(file_path, category)
    assert isinstance(indicators, list) and len(indicators) == 24
