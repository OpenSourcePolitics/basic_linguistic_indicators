"""
This file checks that the template is correctly updated with the indicators found it the data
"""
import os
import pytest
from openpyxl import load_workbook
from linguistic_database.ldb_creation import update_template_xlsx

TEST_PATH_LDB_CREATION = os.path.split(os.path.realpath(__file__))[0]
STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(TEST_PATH_LDB_CREATION, "../test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(TEST_PATH_LDB_CREATION, "../test_data/word_frequency_test2.json")
CONFIG_UPDATE_XLSX_VALIDATION = [(STORED_TEST_DATA_MULTI_CATEGORIES, "category 3",
                                  ["test", 63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (STORED_TEST_DATA_MULTI_CATEGORIES, None,
                                  ["test", 321, 0, 0, 0, 0, 0, 30, 0, 0, 0, 49, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (STORED_TEST_DATA_ONE_CATEGORY, "category 1",
                                  ["test2", 218, 0, 0, 0, 0, 0, 95, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                 (STORED_TEST_DATA_ONE_CATEGORY, None,
                                  ["test2", 218, 0, 0, 0, 0, 0, 95, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
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


@pytest.mark.parametrize("file_path, category, output", CONFIG_UPDATE_XLSX_VALIDATION)
def test_update_template(file_path, category, output):
    """
    Checks that all the information that the function update_template_xlsx() is
    supposed to append to the template is correct.
    :param file_path: path to the json object storing the data
    :type file_path: str
    :param category: category specified by the user used to subset the data
    :type category: str
    :param output: ground truth value by config
    :type output: list
    """
    template_path = TEST_PATH_LDB_CREATION + "/../criteria_template.xlsx"
    update_template_xlsx(template_path=template_path, data_file_path=file_path, category=category)
    values, title = get_cells_values('C')
    if category is None:
        category = "whole_data"
    assert values == output and title == category
