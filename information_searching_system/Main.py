"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: This module is the main function for user login s
"""


import re
import os
import random
from Admin import Admin
from User import User
from Instructor import Instructor
from Student import Student
from Review import Review
from Course import Course


def show_menu(user_role):  ## this function is used to show the menu if the user login successfully
    return ('''{} login successfully!
                    Welcome{}.Your role is {}.
                    Please enter{} command for further service:
                    1. EXTRACT_DATA
                    2. VIEW_COURSES
                    3. VIEW_USERS
                    4. VIEW_REVIEWS
                    5. REMOVE_DATA'''.format(user_role, user_role, user_role, user_role))


## if user login successfully, the fuction will return the menu contain the role of user, i.e. student or admin

def process_operations(user_object):## this function is
    if isinstance(user_object, Admin):  ## using isinstance function to check whether the user_object is instance from class Admin
          ## if the user is admin, then we can check which number that it enter in show_menu function
        while 1:
            user_input = input(show_menu('Admin'))## using while loop
            if user_input == '1':  ## if admin enter num '1'
                user_object.extract_info()  ##call method extract_info from admin class
            elif user_input.startswith('2'):  ## if the admin enter string start with 2
                user_object.view_courses([user_input.split(' ')[1], user_input.split(' ')[2]])  ## call method view courses from admin class；split the user input to match the keyword for view course
            elif user_input == '3':
                user_object.view_users()  ## if admin enter '3', call the method view_users from admin class
            elif user_input.startswith('4'):  ## if admin enter string start with 4
                user_object.view_reviews()([user_input.split()[1], user_input.split()[2]])  ## call method view reviews from admin class,split the admin input string to match the key word for view rviews
            elif user_input == '5':
                user_object.remove_data()  ## if admin enter 5,call method remove data from admin class
            elif user_input == 'logout':  ## if admin enter logout, print byebye message and break the loop
                print('BYEBYE')
                break
            else:
                print('LOGIN FAILED!TRY AGAIN')  ## if the information that entered from admin are not match with any keyword
                continue  ## print error message and continue the loop
    elif isinstance(user_object, Student):  ## using isinstance function to check whether the user_object is instance from class student

        while 1:
            user_input = input(show_menu('Student'))  ## if the user is student, then we can check which number that it enter in show_menu function
            if user_input == '1':## if user enter 1
                user_object.extract_info()## call extract_info methond
                break ##  since student cannot extract information, so raise the inform message and break loop
            elif user_input == '2':
                user_object.view_courses() ## if student enter2, call view course methond


            elif user_input == '3':
                user_object.view_users()## if user enter 3, call view users methond and break
                break
            elif user_input == '4':
                user_object.view_reviews()## if user enter 4, call view review methond
            elif user_input == '5':
                user_object.remove_data()## if user enter 5, call remove data methond and break
                break
            elif user_input == 'logout':#### if user enter logout, print byebye message and break the loop
                print('BYEBYE')
            else:
                print('LOGIN FAILED!TRY AGAIN')## if the information that entered from student are not match with any keyword
                continue         ## print error message and continue the loop
    elif isinstance(user_object, Instructor):
        while 1:
            user_input = input(show_menu('Instructor'))
            if user_input == '1': ## if user enter 1 call extract_info methond
                user_object.extract_info()
                break
            elif user_input == '2':    ## if student enter2, call view course methond
                user_object.view_courses()
                continue
            elif user_input == '3':
                user_object.view_users()## if user enter 3, call view users methond and break
                break
            elif user_input == '4':
                user_object.view_reviews()## if user enter 4, call view review methond
            elif user_input == '5':
                user_object.remove_data()## if user enter 5, call remove data methond and break
                break
            elif user_input == 'logout':#### if user enter logout, print byebye message and break the loop
                print('BYEBYE')
            else:
                print('LOGIN FAILED!TRY AGAIN')## if the information that entered from student are not match with any keyword
                continue ## print error message and continue the loop


def main():

    while 1:
        login_input = input('Please input username and password to login:\n\n(format:username password, enter exit for quit)')## get the users input

        if login_input == 'exit': ##if user enter"exit", print goddbye message and break loop
            print("GOODBYE")
            break

        elif login_input.split(' ')[0] == ' ' or login_input.split(' ')[1] == ' ': ## if user do not enter username or password

            print('username or password incorrect, TRYAGAIN!')## print error message and continue the loop
            continue

        else: ##if user enter the correct information
            temp_user = User('', login_input.split(' ')[0], login_input.split(' ')[1]) ##tranfer the message to the user class
            login_info = temp_user.login() ## after instance the user class, call login methond to check the role of user
            login_result = login_info[0]
            login_user_role = login_info[1]
            login_user_infor = login_info[2]
            if not login_result: ## if login result is false
                print('username or password incorrect, TRYAGAIN!') ## print error message

            else:
                login_user_infor = login_user_infor.split(';;;') ## if the login result is true
                if login_user_role == 'Student': ## if the user is student

                    student_login = Student(login_user_infor[0], login_user_infor[1], login_user_infor[2],
                                            login_user_infor[3], login_user_infor[4],
                                            login_user_infor[5], login_user_infor[6]) ## transit the user information to student class


                    process_operations(student_login) ##call process_opreation to check the user input and call information
                elif login_user_role == 'Instructor':## if the user is instructor
                    instructor_login = Instructor(login_user_infor[0], login_user_infor[1], login_user_infor[2],
                                                  login_user_infor[3], login_user_infor[4],
                                                  login_user_infor[5], login_user_infor[6])## transit the user information to student class

                    process_operations(instructor_login)##call process_opreation to check the user input and call information
                elif login_user_role == 'Admin':## if the user is admin
                    admin_login = Admin(login_user_infor[0], login_user_infor[1], login_user_infor[2]) ## transit the user information to student class

                    process_operations(admin_login) ##call process_opreation to check the user input and call information


if __name__ == "__main__":
    print('WELCOME TO OUR check check check check check check  SYSTEM!') ## print welcome message

    admin = Admin(-1,'adm','adm') ##mannually regist admin


    admin.register_admin()## after inhertance the class and transit user input to admin class, and call fuction register admin


    main() ## call function mean


