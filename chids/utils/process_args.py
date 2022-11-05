import os
from urllib.parse import urlparse
from string import digits
from chids.shared.constants import *
from chids.conf.config import PATH_LENGTH


def get_filepath(raw_arg, category):

    if category == MODE_SO:
        file_path = raw_arg[5:]

    if category == MODE_EX:
        file_path = raw_arg[9:]

    if category == MODE_CL:
        file_path = raw_arg[4:]

    return process_path(file_path)


def process_path(file_path_i):

    if "(" in file_path_i and ")" in file_path_i:
        file_path_between_par = file_path_i[file_path_i.find("(") + 1:file_path_i.find(")")]
        file_path_before_par = file_path_i[:file_path_i.find("(")]
        file_path_max = max([file_path_between_par, file_path_before_par], key=len)

        if file_path_i.count("/") > PATH_LENGTH:
            file_path_min = min([file_path_between_par, file_path_before_par], key=len)
            file_path_i = file_path_max.replace(file_path_min, "")
        else:
            file_path_i = file_path_max

    else:
        if file_path_i.count("/") > PATH_LENGTH:
            full_path = urlparse(file_path_i)
            file_path_i = os.path.dirname(full_path.path)

    processed_file_path = file_path_i.rsplit('/')
    path_last_element = processed_file_path[-1]

    # we clean the path from random characters and numbers
    if path_last_element.islower():
        processed_file_path[-1] = path_last_element.translate({ord(k): None for k in digits})
        processed_file_paths = '/'.join(processed_file_path)
    else:
        processed_file_paths = '/'.join(processed_file_path[:-1])

    return processed_file_paths
