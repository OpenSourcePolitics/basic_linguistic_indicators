"""
This file will be responsible of the linguistic
database creation. It will follow the information available in the template.
"""
from openpyxl import load_workbook
from linguistic_database.ldb_information_retrieval import prepare_data


def write_specific_cell(worksheet, list_values, column_letter):
    """
    For a given list of values this function will write the information from row 6 to 29 in a specified column
    (identified with the parameter column_letter) in a .xlsx file : criteria_template.xlsx.
    :param worksheet: current active worksheet
    :param list_values: list of values to append to the file (linguistic indicators)
    :type list_values: list
    :param column_letter: column identifier
    :type column_letter: str
    """
    index = 0
    for row in range(6, 30):
        column_id = column_letter + '{}'.format(row)
        worksheet[column_id] = list_values[index]
        index += 1


def update_template_xlsx(template_path: str, parsed_word_frequency_data: dict, category=None):
    """
    Updates the file criteria_template.xlsx:
        - appends the name of the data file
        - the linguistic indicators found in the data
        - names the worksheet with the category specified by the user
    """
    workbook = load_workbook(filename=template_path)
    worksheet = workbook.active
    if category is not None:
        worksheet.title = category
    else:
        worksheet.title = "whole_data"
    # worksheet["C2"] = filename
    list_values = prepare_data(parsed_word_frequency_data)
    write_specific_cell(worksheet=worksheet, list_values=list_values, column_letter='C')
    workbook.save(filename=template_path)
