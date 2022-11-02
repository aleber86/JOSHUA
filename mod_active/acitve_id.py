#!/usr/bin/env python3

import numpy as np

from os.path import dirname, realpath, join
import sys

Dir_prog = dirname(realpath(__file__))


def CHAT_ID_VALIDATE():
    data_dict = {}
    with open(f"{Dir_prog}/CHAT_ID_TABLE", "r") as file_cripto:
        file_cripto.readline()
        while True:
            data = file_cripto.readline()
            if data == "":
                break
            else:
                values = data.split(6*" ")
                if values != ["\n"]:
                    data_dict[int(values[0])] = {"status": values[1], "code":values[2][:-1]}
    return data_dict

def validate_user(chat_id):
    base_matrix = np.matrix([[47,13,23,7,5], [97,59,11,37,39], [17,23,31,67,19],
                             [61,73,71,53,43],[89,83,59,41,97]], dtype = np.int64)

    base_matrix = base_matrix.reshape(5,5)
    chat_id_str = str(chat_id)
    len_id = len(chat_id_str)
    offset = len_id%5
    if offset!=0:
        chat_id_str = f"{chat_id_str}{(5-offset)*'0'}"
    id_split = []
    base_index = 0
    top_index = 5
    value_to_append = 0
    try:
        while value_to_append != "":
            value_to_append = chat_id_str[base_index:top_index]
            int(value_to_append)
            sub_list = []
            for digit in value_to_append:
                sub_list.append(int(digit))
            id_split.append(sub_list)
            base_index+=5
            top_index+=5
    except ValueError:
        pass
    id_split = np.matrix(id_split, dtype=np.int64)
    id_split = np.transpose(id_split)
    half_step = np.matmul(base_matrix, id_split)
    half_step = np.matmul(np.transpose(half_step), np.transpose(base_matrix))
    matrix_reverse = np.copy(base_matrix)
    matrix_reverse = matrix_reverse.tolist()
    for index,row in enumerate(matrix_reverse):
        rev = reversed(row)
        rev = [i for i in rev]
        matrix_reverse[index] = rev
    matrix_reverse = np.matrix(matrix_reverse, dtype=np.int64)
    half_step = np.matmul(np.transpose(matrix_reverse), np.transpose(half_step))
    row,col = half_step.shape
    str_half = ""
    base_char = 0
    for i in np.nditer(half_step, order='C'):
        size = int(str(i)[0:1])
        char_size = chr(size+96)
        str_half = f"{str_half}{str(i)}{char_size}"
    str_half = f"{str_half}{row}{col}"

    return str_half

def user_validation(id_value):
    data_from_file = CHAT_ID_VALIDATE()
    try:
        status = data_from_file[id_value]["status"]
        if (status == "ACTIVE" and validate_user(id_value) == data_from_file[id_value]["code"]):
            return True
        else:
            return False

    except KeyError as error:
        return False

def validate_new_user():
    space = 6*" "
    chat_id = input("Inserte el numero de chat: ")
    ban_or_active = input("Validar (VALID) / Banear (BAN): ")
    try:
        chat_id = int(chat_id)
        ban_or_active = ban_or_active.lower()
        data_from_file = CHAT_ID_VALIDATE()
        if ban_or_active == "valid":
            code = validate_user(chat_id)
            data_from_file[chat_id] = {"status" : "ACTIVE", "code" : code}
        elif ban_or_active == "ban":
            data_from_file[chat_id] = {"status" : "***BAN", "code" : "*"}
        with open(f"CHAT_ID_TABLE", "w") as file_cripto:
            file_cripto.write("#Chat_id        #Status     #CODE\n")
            for it, value in data_from_file.items():
                file_cripto.write(f"{it}{space}{value['status']}{space}{value['code']}\n")
    except TypeError:
        pass

if __name__ == '__main__':
    validate_new_user()




