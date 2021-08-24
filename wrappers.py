from numpy import zeros
from zipfile import ZipFile
import os.path
from shutil import rmtree

def read_table_horiz(initial_row, initial_col, final_row, final_col, header_col, name_sheet, book):
    """
    Lee una tabla con orientación horizontal.

    """
    sheet = book[name_sheet]
    input_global = {}
    cont = 0
    for i in range(initial_col, final_col + 1):
        aux_dict = {}
        for j in range(initial_row, final_row + 1):
            key = sheet.cell(j, header_col).value
            value = sheet.cell(j, i).value
            if value == None:
                value = None
            aux_dict.update({key: value})
        if final_col - header_col == 1:
            input_global = aux_dict
        else:
            input_global.update({cont: aux_dict})
            cont = cont + 1
    return input_global