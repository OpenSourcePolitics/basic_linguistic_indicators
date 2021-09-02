"""
This file is checks that the information retrieval process is working correctly
"""
import os
import pytest
from utils.word_frequency_data_interface import LocalWordFrequencyDataLoading
from linguistic_database.ldb_information_retrieval import get_total_word_count, specific_vocabulary_retrieval, \
    multi_criteria_extraction, get_conditional_markers, prepare_data
from main import get_parsed_data

TEST_LDB_IR = os.path.split(os.path.realpath(__file__))[0]
STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(TEST_LDB_IR, "../test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(TEST_LDB_IR, "../test_data/word_frequency_test2.json")

word_frequencies_by_cat_object_config_1 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_MULTI_CATEGORIES).load()
word_frequencies_by_cat_object_config_2 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_ONE_CATEGORY).load()

CONFIG_SUM = [(word_frequencies_by_cat_object_config_1, "category 3", 63),
              (word_frequencies_by_cat_object_config_1, None, 321),
              (word_frequencies_by_cat_object_config_2, "category 1", 218),
              (word_frequencies_by_cat_object_config_2, None, 218)]

CONFIG_WORD_RETRIEVAL = [(word_frequencies_by_cat_object_config_1, ["word1", "word2", "not_in_list"],
                          "category 3", [5, 20, 0]),
                         (word_frequencies_by_cat_object_config_1,
                          ["word1", "word2", "not_in_list"], None, [95, 31, 0]),
                         (word_frequencies_by_cat_object_config_2,
                          ["word1", "word2", "not_in_list"], "category 1", [1, 5, 0]),
                         (word_frequencies_by_cat_object_config_2,
                          ["word1", "word2", "not_in_list"], None, [1, 5, 0])]

CONFIG_CONDITIONAL_MARKERS = [(word_frequencies_by_cat_object_config_1, "category 2", 30),
                              (word_frequencies_by_cat_object_config_1, None, 30),
                              (word_frequencies_by_cat_object_config_2, "category 1", 95),
                              (word_frequencies_by_cat_object_config_2, None, 95)]

CONFIG_DATA_PREPARATION = [(word_frequencies_by_cat_object_config_1, "category 2"),
                           (word_frequencies_by_cat_object_config_1, None),
                           (word_frequencies_by_cat_object_config_2, "category 1"),
                           (word_frequencies_by_cat_object_config_2, None)]


@pytest.mark.parametrize("word_frequencies_by_cat_object, category, output", CONFIG_SUM)
def test_get_total_count(word_frequencies_by_cat_object, category, output):
    """
    Checks that the sum of the values is correct
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: int
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    dict_sum = get_total_word_count(parsed_data.preprocessed)
    assert isinstance(dict_sum, int) and dict_sum == output


@pytest.mark.parametrize("word_frequencies_by_cat_object, word_list, category, output", CONFIG_WORD_RETRIEVAL)
def test_specific_word_retrieval(word_frequencies_by_cat_object, word_list, category, output):
    """
    Checks that specific_word_retrieval works properly :
        - retrieve the values of the words specified as inputs
        - appends 0 if the words is not in the data
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param word_list: list of linguistic indicators
    :type word_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    words_frequency = specific_vocabulary_retrieval(parsed_data.preprocessed, word_list)
    assert isinstance(words_frequency, list) and words_frequency == output


@pytest.mark.parametrize("word_frequencies_by_cat_object, word_list, category, output", CONFIG_WORD_RETRIEVAL)
def test_multi_criteria_extraction(word_frequencies_by_cat_object, word_list, category, output):
    """
     Checks that multi_criteria_extraction works properly :
        - output a single metric for the initial words
        - correct type
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param word_list: list of linguistic indicators
    :type word_list: list
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    indicators_frequency = multi_criteria_extraction(parsed_data.preprocessed, word_list)
    assert isinstance(indicators_frequency, int) and indicators_frequency == sum(output)


@pytest.mark.parametrize("word_frequencies_by_cat_object, category, output", CONFIG_CONDITIONAL_MARKERS)
def test_conditional_markers_retrieval(word_frequencies_by_cat_object, category, output):
    """
    Checks that the conditional markers retrieval works properly
        - correct output
        - correct type
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    conditional_markers_frequency = get_conditional_markers(parsed_data.preprocessed)
    assert isinstance(conditional_markers_frequency, int) and conditional_markers_frequency == output


@pytest.mark.parametrize("word_frequencies_by_cat_object, category", CONFIG_DATA_PREPARATION)
def test_data_preparation(word_frequencies_by_cat_object, category):
    """
    Checks the behavior of the data preparation function
        - correct number of values
        - correct type
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param category: category specified by the user used to subset the data
    :type category: str
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    indicators = prepare_data(parsed_data.preprocessed)
    assert isinstance(indicators, list) and len(indicators) == 24
