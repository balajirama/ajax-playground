from flask import flash
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")
AT_LEAST_ONE_NUM_REGEX = re.compile(r"^.*[0-9]+.*")
AT_LEAST_ONE_CAP_REGEX = re.compile(r"^.*[A-Z]+.*")

def is_age_over(num, dob):
    if(type(dob) == type('')):
        if dob != '':
            dob = datetime.strptime(dob, '%Y-%m-%d')
        else:
            return False
    elif type(dob) == type(datetime.now()):
        dob = dob
    else:
        return False
    year = dob.year + num
    nth_bday = datetime.strptime(f"{year}-{dob.month}-{dob.day}", "%Y-%m-%d")
    today = datetime.today()
    return (today - nth_bday).days >= 0

def copy_immutable_dict(immutable_dict, **kwargs):
    result_dict = dict()
    for item in immutable_dict.keys():
        result_dict[item] = immutable_dict[item]
    for param, value in kwargs.items():
        result_dict[param] = value
    return result_dict

def get_age(dob):
    age = -1
    while(is_age_over(age+1, dob)):
        age += 1
    return age

def is_valid_password(request_form, categories=['password', 'confirm']):
    is_valid = True
    if len(request_form[categories[0]]) < 8:
        flash("Password must be at least eight characters", categories[0])
        is_valid = False
    if not(AT_LEAST_ONE_NUM_REGEX.match(request_form[categories[0]]) and AT_LEAST_ONE_CAP_REGEX.match(request_form[categories[0]])):
        flash("Password must contain at least one capital letter and one digit", categories[0])
        is_valid = False
    if (request_form[categories[1]] == "") or (request_form[categories[0]] != request_form[categories[1]]):
        flash("Passwords do not match", categories[1])
        is_valid = False
    return is_valid

import copy

def add_column_to_query_result(list_of_dict, column=None, funcname=None, args=[]):
    """
    This function can be used to add a column to a SELECT query result where
    you use the value in one or more of the existing columns to create a new
    column. For example:

        add_column_to_quer_result(query_result, column='special', funcname=some_function, args=['col1', 'col2'])

    query_result : a list of dictionaries, typically the result of a SELECT query.
    column       : Optional argument. If not specified, the function will return query_result as it is
                   when specified, it this is the name of the column that will be added to the query_result
    funcname     : Name of the function that will generate the data for that column. This can be any function
                   user-defined or built-in function. No quotes.
    args         : This is a list of arguments. If any of the arguments is the name of an existing column in 
                   query_result, then the value in that column will be used.

    """
    return_dict = copy.deepcopy(list_of_dict)
    if column==None or funcname==None:
        return return_dict
    for row in return_dict:
        funcarg = list()
        for elem in args:
            if elem in row.keys():
                funcarg.append(row[elem])
            else:
                funcarg.append(elem)
        row[column] = funcname(funcarg)
    return return_dict


