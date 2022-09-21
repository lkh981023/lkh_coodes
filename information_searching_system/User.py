"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: this module is design for user login system.
------------------------------
 def generate_unique_user_id(self)
 return the random genrated 10 digit number
 ----------------------------
 def encryption(self, input_password)
 encrypted input_password
 -------------------------------
 def login(self)
 design for check login user role, user infor and login result
 -----------------------
 def extract_info(self)
 design for user want to extract others information and will print no permission message
 -------------------------------
 def view_courses(self, args=[])
 design for user want to view other course and print no permission message
 ------------------------------------
 def view_users(self)
design for user who want to view others infor and print no permission message
---------------------------------------
 def remove_data(self)
 design for user who want to remove data and print no permission message
"""

import random


class User:

    def __init__(self, _id=0, username='', password=''):
        self.id = _id
        self.username = username
        self.password = password

    def generate_unique_user_id(self): ## this methond is used for generate random user_id for user who doesn't have id

        admins_info = []
        students_info = []
        instructor_info = []
        with open('./data/result/user_admin.txt', 'a+') as admin_f:

            for line in admin_f:
                admins_info.append(line)
        with open('./data/result/user_student.txt', 'a+') as student_f:
            for line in student_f:
                students_info.append(line)
        with open('./data/result/user_instructor.txt', 'a+') as instructor_f:
            for line in instructor_f:
                instructor_info.append(line)
        users = admins_info + students_info + instructor_info ## first generate all users information from three result files
        while 1:
            users_id = str(random.randint(1000000000, 9999999999)) ## using randint to generate 10 digit id
            if users_id not in users: ## if the random id not in files
                return users_id ## return user_id

    def encryption(self, input_password): ## this methond is used for encrypted password

        self.input_password = input_password
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        indx = len(input_password) % len(
            all_punctuation)  # first to get the length of string "all_punctuation" and the length of user input string to confirm the first character location
        first_charac = all_punctuation[indx]  # the first character that used to encryption
        second_charac = all_punctuation[
            len(input_password) % 5]  # the location of second character that used to encryption
        third_charac = all_punctuation[
            len(input_password) % 10]  # the location of third character that used to encryption
        encrypted_pd = ''  # add new raw data and named of encrypted_pd, the data type is string
        for letter in range(len(input_password)):  # using for loop to check the specific postion in string
            if letter % 3 == 0:  # when the length of input is 3n
                encrypted_pd = encrypted_pd + first_charac + input_password[letter] + first_charac
            elif letter % 3 == 1:  # when the length of input is 3n+1
                encrypted_pd = encrypted_pd + second_charac * 2 + input_password[letter] + second_charac * 2
            elif letter % 3 == 2:  # when the length of input is 3n+2
                encrypted_pd = encrypted_pd + third_charac * 3 + input_password[letter] + third_charac * 3
            elif letter % 3 == 3:  # when the length of input is 3n+3
                encrypted_pd = encrypted_pd + first_charac + input_password[letter] + first_charac
            encrypted_pd = '^^^' + encrypted_pd + '$$$'  # add required character on encrpted password on left and right respectively
        return encrypted_pd

    def login(self): ## this methond is used for check user information when user login system

        with open('./data/result/user_student.txt', 'r') as user_student_f:
            students_infor = user_student_f.read()

        with open('./data/result/user_admin.txt', 'r') as user_admin_f:
            admin_infor = user_admin_f.read()
        with open('./data/result/user_instructor.txt', 'r') as user_instructor_f:
            instructor_infor = user_instructor_f.read() ## open files from three result file
        login_result = False
        login_user_role = ''
        login_user_infor = '' ## initialize the variable
        encrypted_pswd = self.encryption(self.password) ## when user input password, encrypted the input password and compare with the password has already encrypted in files
        if self.username in admin_infor.split('\n'):
            for item in admin_infor:
                if self.username in item and encrypted_pswd in item:
                    login_result = True
                    login_user_role = 'Admin'
                    login_user_infor = item
                    break ## if the username and encrypted password  in student result file, confirm the user role is student, login result is true and login user information in file
        elif self.username in students_infor.split('\n'):
            for item in students_infor:
                if self.username in item and encrypted_pswd in item:
                    login_result = True
                    login_user_role = 'Student'
                    login_user_infor = item
                    break ## if the username and encrypted password  in admin result file, confirm the user role is student, login result is true and login user information in file

        elif self.username in instructor_infor:

            for item in instructor_infor.split('\n'):

                if self.username in item and encrypted_pswd in item:
                    login_result = True
                    login_user_role = 'Instructor'
                    login_user_infor = item
                    break## if the username and encrypted password  in instructor result file, confirm the user role is student, login result is true and login user information in file
        else:
            return 'username or password incorrect'    ## if the username and password does not match, return incorrect message

        return login_result, login_user_role, login_user_infor

    def extract_info(self):

        return 'You have no permission to extract information'  ## this methond is used when user want to extract information and will print error message

    def view_courses(self, args=[]):
        return 'You have no permission to view courses' ## this methond is used when user want to view courses doesn't from itself and will print error message

    def view_users(self):
        return 'You have no permission to view users'## this methond is used when user want to view users and will print error message

    def view_reviews(self, args=[]):
        return 'You have no permission to view reviews' ## this methond is used when user want to view reviews doesn't from itself and will print error message

    def remove_data(self):
        return 'You have no permission to remove data' ## this methond is used when user want to remove data and will print error message

    def __str__(self):
        return '{};;;{};;;{}'.format(self.id, self.username, self.password)



