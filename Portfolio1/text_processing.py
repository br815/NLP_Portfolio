# Name: Bushra Rahman
# Class: CS 4395.001
# Assignment: Text Processing with Python
# Due date: 2/4/23

import sys
import pathlib
import re
import pickle


# definition of Person class
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # display method called in main() for each Person in employees.pickle
    def display(self):
        print('\nEmployee id: ', self.id)
        print('        ', self.first, self.mi, self.last)
        print('        ', self.phone)
# end of Person class


# this function takes a list as input
# and outputs a dictionary.
def process_lines(text):
    # initialize dictionary
    dict_employees = {}

    # process each string str_x in the list of text
    for str_x in text:
        # split on comma to get text fields as variables
        tokens = str_x.split(",")

        # first and last name modified to be in capital case
        last_name = tokens[0].lower().capitalize()
        first_name = tokens[1].lower().capitalize()

        # modify MI to be uppercase or X if not found
        if tokens[2] == '':
            middle_initial = 'X'
        else:
            middle_initial = tokens[2].upper()

        # ID token should be 2 letters followed by 4 digits
        emp_id = tokens[3]
        match = re.fullmatch('[A-Za-z]{2}\\d{4}', emp_id)
        while not match:
            print("Invalid ID:", emp_id)
            print("ID is two letters followed by 4 digits")
            emp_id = input("Please enter a valid id:")
            match = re.fullmatch('[A-Za-z]{2}\\d{4}', emp_id)

        # phone number should be in form 123-456-7890
        phone_num = tokens[4]
        match = re.fullmatch('\\d{3}-?\\d{3}-?\\d{4}', phone_num)
        while not match:
            print("Phone", phone_num, "is invalid")
            print("Enter phone number in form 123-456-7890")
            phone_num = input("Enter phone number:")
            match = re.fullmatch('\\d{3}-?\\d{3}-?\\d{4}', phone_num)
        match = re.fullmatch('\\d{3}-\\d{3}-\\d{4}', phone_num)
        # if phone_num has the right # of digits but no dashes,
        # just re-concatenate it with dashes.
        if not match:
            first_3 = phone_num[0:3]
            second_3 = phone_num[3:6]
            last_4 = phone_num[6:10]
            phone_num = first_3 + '-' + second_3 + '-' + last_4

        # create Person object
        employee = Person(last_name, first_name, middle_initial, emp_id, phone_num)
        # print error for duplicate key
        if emp_id in dict_employees:
            print("ERROR: Duplicate employee ID. Cannot add this employee to the dictionary.")
        else:
            # add employee to dictionary
            dict_employees[emp_id] = employee
    # end of for loop

    return dict_employees
# end of process_lines()


# main()
if __name__ == '__main__':
    # user must specify a sysarg, otherwise quit
    if len(sys.argv) < 2:
        # the relative path "data/data.csv" is specified under Parameters in "Edit Configurations"
        print('Please enter a filename as a system arg')
        quit()

    rel_path = sys.argv[1]  # save the user-inputted relative path

    # pathlib joins relative path to current working directory for cross-platform file opening
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        # text_in is a list of each string from the input file f, split on newlines
        text_in = f.read().splitlines()

    # process_lines is our text processing function
    # employees is a dictionary of the employees
    # [1:] skips header line
    employees = process_lines(text_in[1:])

    # pickle the employees
    file = open('employees.pickle', 'wb')
    pickle.dump(employees, file)
    file.close()

    # read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\n\nEmployee list: ')
    for employee_id in employees_in.keys():
        # display() function comes from Person class
        employees_in[employee_id].display()
# end of main()
