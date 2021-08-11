"""
This file checks that the template is correctly updated with the indicators found it the data
"""
import os
import pytest
from openpyxl import load_workbook
from utils.word_frequency_data_interface import LocalWordFrequencyDataLoading
from linguistic_database.ldb_creation import update_template_xlsx
from main import get_parsed_data
TEST_PATH_LDB_CREATION = os.path.split(os.path.realpath(__file__))[0]
STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(TEST_PATH_LDB_CREATION, "../test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(TEST_PATH_LDB_CREATION, "../test_data/word_frequency_test2.json")
word_frequencies_by_cat_object_config_1 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_MULTI_CATEGORIES).load()
word_frequencies_by_cat_object_config_2 = LocalWordFrequencyDataLoading(STORED_TEST_DATA_ONE_CATEGORY).load()

CONFIG_UPDATE_XLSX_VALIDATION = [(word_frequencies_by_cat_object_config_1, "category 3",
                                  ["test preprocessed",
                                   63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (word_frequencies_by_cat_object_config_1, None,
                                  ["test preprocessed",
                                   321, 0, 0, 0, 0, 0, 30, 0, 0, 0, 49, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (word_frequencies_by_cat_object_config_2, "category 1",
                                  ["test preprocessed",
                                   218, 0, 0, 0, 0, 0, 95, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (word_frequencies_by_cat_object_config_2, None,
                                  ["test preprocessed",
                                   218, 0, 0, 0, 0, 0, 95, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                                 ]


def get_cells_values(column_letter):
    """
    Used to retrieve the values append in the template to check the results of
    update_template_xlsx()
    :param column_letter: column identifier
    :type column_letter: str
    :return: values append in the file, title of the worksheet
    :rtype: tuple
    """
    written_values = []
    template_path = TEST_PATH_LDB_CREATION + "/../criteria_template.xlsx"
    workbook = load_workbook(filename=template_path)
    worksheet = workbook.active
    written_values.append(worksheet["C2"].value)
    for i in range(6, 30):
        written_values.append(worksheet["{}{}".format(column_letter, i)].value)
    return written_values, worksheet.title


@pytest.mark.parametrize("word_frequencies_by_cat_object, category, output", CONFIG_UPDATE_XLSX_VALIDATION)
def test_update_template(word_frequencies_by_cat_object, category, output):
    """
    Checks that all the information that the function update_template_xlsx() is
    supposed to append to the template is correct.
    :param word_frequencies_by_cat_object: Data structure storing the preprocessed data
    and the non preprocessed data loaded with LocalWordFrequencyDataLoading
    :type word_frequencies_by_cat_object: WordFrequenciesByCategory
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    parsed_data = get_parsed_data(word_frequencies_by_cat_object, category)
    template_path = TEST_PATH_LDB_CREATION + "/../criteria_template.xlsx"
    update_template_xlsx(template_path=template_path,
                         parsed_word_frequency_data=parsed_data.preprocessed, category=category)
    values, title = get_cells_values('C')
    if category is None:
        category = "whole_data"
    assert values == output and title == category
