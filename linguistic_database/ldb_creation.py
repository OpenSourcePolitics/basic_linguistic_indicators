"""
This file will be responsible of the linguistic
database creation. It will follow the information available in the template.
"""
import os
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


def update_template_xlsx(template_path, data_file_path, category=None):
    """
    Updates the file criteria_template.xlsx:
        - appends the name of the data file
        - the linguistic indicators found in the data
        - names the worksheet with the category specified by the user
    :param template_path: path to the template to update
    :type template_path: str
    :param data_file_path: path to the json storing the data
    :type data_file_path: str
    :param category: category used to subset the data
    :type category: str
    """
    filename = os.path.basename(os.path.normpath(os.path.splitext(data_file_path)[0]))
    filename = filename[15:].replace("_", " ")
    workbook = load_workbook(filename=template_path)
    worksheet = workbook.active
    if category is not None:
        worksheet.title = category
    else:
        worksheet.title = "whole_data"
    worksheet["C2"] = filename
    list_values = prepare_data(data_file_path, category)
    write_specific_cell(worksheet=worksheet, list_values=list_values, column_letter='C')
    workbook.save(filename=template_path)
