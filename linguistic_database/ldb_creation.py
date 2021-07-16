"""
This file will be responsible of the linguistic
database creation. It will follow the information available in the template.
"""
import os
from openpyxl import load_workbook
from linguistic_database.ldb_information_retrieval import prepare_data


def write_specific_cell(worksheet, list_values, column_letter):
    index = 0
    for row in range(6, 30):
        column_id = column_letter + '{}'.format(row)
        worksheet[column_id] = list_values[index]
        index += 1


def update_template_xlsx(template_path, data_file_path):
    filename = os.path.basename(os.path.normpath(os.path.splitext(data_file_path)[0]))
    filename = filename[15:].replace("_", " ")
    workbook = load_workbook(filename=template_path)
    worksheet = workbook.active
    worksheet["C2"] = filename
    list_values = prepare_data(data_file_path)
    write_specific_cell(worksheet=worksheet, list_values=list_values, column_letter='C')
    workbook.save(filename=template_path)
