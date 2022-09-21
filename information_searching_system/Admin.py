"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: This class is design for user admin to use the program
for opreations i.e: extract other user data and clear data, view all users informations
"""

import re
import os
from User import User
from Course import Course
from Review import Review


class Admin(User):

    def __init__(self, _id=-1, username='', password=''):
        User.__init__(self, _id, username, password)

    def register_admin(self):  ## using for regist admin
        try:
            with open('./data/result/user_admin.txt','r') as file1:
                admin_info = file1.read()
                if self.username not in admin_info:
                    with open('./data/result/user_admin.txt','a+') as file1:
                        file1.write('{};;;{};;;{}'.format(self.id,self.username,self.encryption(self.password)) + '\n')
        except FileNotFoundError:
            with open('./data/result/user_admin.txt','w+') as file1:
                file1.write('{};;;{};;;{}'.format(self.id, self.username, self.encryption(self.password)) + '\n')


        # with open('./data/result/user_admin.txt','a+') as add_in_admin_f:  ## open the file for saving admin information
        #     if self.username not in add_in_admin_f.read():  ## if the username not in file
        #         pswd_en = self.encryption(self.password)  ## encrypted the password
        #         add_in_admin_f.write('{};;;{};;;{}'.format(self.id, self.username, pswd_en))  ## write information in file for register

    def extract_course_info(self):  ## using for extract course infor from raw data file

        check_data = open('./data/course_data/raw_data.txt','r')  ## open raw data and using regex to match the needed information
        course_info_lst = []
        check_course_info = check_data.read()
        course_id = re.findall(r'"course","id":(\d+?),', check_course_info)
        course_title = re.findall(r'"course","id":\d+?,"title":"(\S.*?)",', check_course_info)
        image_100x100 = re.findall(r'practice_tests":\d+?,"image_50x50":"\w.*?","image_100x100":"(\w.*?)"',
                                   check_course_info)
        headline = re.findall(r'"headline":"(\S.*?)",', check_course_info)
        num_of_subscribers = re.findall(r'"num_subscribers":(\d{0,100}),', check_course_info)
        avg_rating = re.findall(r'"avg_rating":(\d.*?),', check_course_info)
        course_content_length = re.findall(r'"content_info_short":(.*?)\s\w.*?,', check_course_info)
        for indx in range(
                len(avg_rating)):  ## since the lenth of information are all same, then using index to get the info and saving to list
            course_info_lst.append('{};;;{};;;{};;;{};;;{};;;{};;;{}'.format(course_id[indx], course_title[indx],
                                                                             image_100x100[indx], headline[indx],
                                                                             num_of_subscribers[indx],
                                                                             avg_rating[indx],
                                                                             course_content_length[indx]))
        write_in_file = open('./data/result/course.txt', 'w')
        write_in_file.write('\n'.join(course_info_lst))  ## write the information to file
        check_data.close()
        write_in_file.close()  ## close files
        check_data.close()

    def extract_review_info(self):  ## using for extract review information

        rev_data = []
        for item in os.listdir('./data/review_data/'):  ## using for loop to iterate files

            check_rev = open('./data/review_data/' + item)
            review_extract = check_rev.read()  ## open and read files for extract information while using regex
            review_id = re.findall(r'"_class": "course_review", "id": (\d{0,10}),', review_extract)
            review_content = re.findall(r'"_class": "course_review", \S.*?, "content": "(.*?)",', review_extract)
            review_rating = re.findall(r'"_class": "course_review", \S.*?, "rating": (.*?),', review_extract)

            for indx in range(len(review_id)):  ## append the informations to list
                rev_data.append('{};;;{};;;{};;;{}'.format(review_id[indx], review_content[indx]
                                                           , review_rating[indx], item[:-5]))
        with open('./data/result/course_review.txt', 'w') as review_file:

            review_file.write('\n'.join(rev_data))  ## write in file
            check_rev.close()

    def extract_student_info(self):  ## this methond is useing for extract student information from review fies
        student_data = []
        for item in os.listdir(
                './data/review_data/'):  ## using for loop to iterate files for get information of stident
            with open(
                    './data/review_data/' + item) as student_extract:  ## open and read files for extract information while using regex
                student_extract = student_extract.read()
                student_review_id = re.findall(r'"_class": "course_review", "id": (\d{0,10}),', student_extract)
                student_inf = re.findall(r'"user_modified": "\w.*?", "user": \{(.*?)\},', student_extract)
            for indx in range(len(student_inf)):

                if re.search(r'"id": (\d{0,10}),', student_inf[0]) is None:  ## if student do not have is, call menthond from panrentc  class to generate id

                    student_id = self.generate_unique_user_id()
                else:
                    student_id = re.search(r'"id": (\d{0,10}),', student_inf[indx])[1]  ## if student have id, match it student id

                student_username = re.search(r'"display_name": "(.*?)"', student_inf[indx])[1]
                student_username = student_username.lower().replace(' ', '_')
                student_initials = re.search(r'"initials": "(.*?)"', student_inf[indx])[1]
                student_pswd = self.encryption(student_initials.lower() + student_id + student_initials.lower())
                student_image = re.search(r'"image_50x50": "(\w.*?)",', student_inf[indx])[1]
                student_title = re.search(r'"title": "(\S.*?)",', student_inf[indx])[1]

                student_infor = '{};;;{};;;{};;;{};;;{};;;{};;;{}'.format(student_id, student_username,
                                                                          student_pswd, student_title,
                                                                          student_image,
                                                                          student_initials, student_review_id[indx])
                student_data.append(student_infor)

        with open('./data/result/user_student.txt', 'w') as student_file:
            student_file.write('\n'.join(student_data))

    def extract_instructor_info(self):  ## using for extract instructor information
        ins_pswd_lst = []
        ins_info = {}
        ins_detail_info = {}
        username_lst = []
        ins_infor_lst = []


        with open('./data/course_data/raw_data.txt',
                  'r') as ins_info_f:  ## open raw data and using regex to get instructor information
            ins_info_extract = ins_info_f.read()
            ins_id = re.findall(r'"visible_instructors":\[\{.*?,"id":(\d{0,10})', ins_info_extract)
            for each in ins_id:
                ins_pswd = self.encryption(each)
                ins_pswd_lst.append(ins_pswd)
            ins_pswd_en = ins_pswd_lst  ## encrypted the password while using excryption methond inherit from parent class
            ins_username = re.findall(r'"visible_instructors":\[\{.*?"display_name":"(\S.*?)".*?\}\]', ins_info_extract)
            for item in ins_username:
                ins_username_new = item.lower().replace(' ', '_')
                username_lst.append(ins_username_new)
            ins_usernames = username_lst
            ins_displayname = re.findall(r'"visible_instructors":\[\{.*?"display_name":"(\S.*?)".*?\}\]',
                                         ins_info_extract)
            ins_job_title = re.findall(r'"visible_instructors":\[\{.*?"job_title":"(\S.*?)".*?\}\]', ins_info_extract)
            ins_image = re.findall(r'"visible_instructors":\[\{.*?"image_100x100":"(\S.*?)".*?\}\]', ins_info_extract)
            ins_course_id = re.findall(r'"course","id":(\d+?),', ins_info_extract)
        for ind in range(len(ins_displayname)):
            if ins_displayname[ind] in ins_info:  ## if the instructor information in the ins_info dict

                ins_info[ins_displayname[ind]]['ins_course_id'] += ins_course_id[ind]  ## append the course id
            else:  ## if not, add the instructor's informtaion to the ins_detail_info dict and write in file

                ins_detail_info['ins_id'] = ins_id[ind]
                ins_detail_info['ins_usernames'] = ins_usernames[ind]
                ins_detail_info['ins_pswd'] = ins_pswd_en[ind]
                ins_detail_info['ins_displayname'] = ins_displayname[ind]
                ins_detail_info['ins_job_title'] = ins_job_title[ind]
                ins_detail_info['ins_image'] = ins_image[ind]
                ins_detail_info['ins_course_id'] = ins_course_id[ind]
                ins_info[ins_displayname[ind]] = ins_detail_info

        for value in ins_info.values():
            ins_ids = value.get('ins_id')
            ins_usernames = value.get('ins_usernames')
            ins_password = value.get('ins_pswd')
            ins_display_name = value.get('ins_displayname')
            ins_job_title = value.get('ins_job_title')
            ins_images = value.get('ins_image')
            ins_courses = '-'.join(value['ins_course_id'])

            with open('./data/result/user_instructor.txt', 'w') as add_in_f:

                add_in_f.write('{};;;{};;;{};;;{};;;{};;;{};;;{}'.format(ins_ids,ins_usernames,ins_password
                                                                         ,ins_display_name,ins_job_title,
                                                                         ins_images,ins_courses) + '\n')

    def extract_info(self):  ## this methond is used for call the methonds for extract information
        self.extract_course_info()
        self.extract_review_info()
        self.extract_student_info
        self.extract_instructor_info()

    def remove_data(self):  ## this methoond is used for remove data from files
        with open('./data/result/user_student.txt', 'r+') as student_file_clear:
            student_file_clear.truncate(0)
        with open('./data/result/user_instructor.txt', 'r+') as instructor_file_clear:
            instructor_file_clear.truncate(0)
        with open('./data/result/review.txt', 'r+') as review_file_clear:
            review_file_clear.truncate(0)
        with open('./data/result/course.txt', 'r+') as admin_file_clear:
            admin_file_clear.truncate(0)

    def view_courses(self, args=[]):  ## this methond is used for admin view course
        if args == '':  ## if admin doesn't enter any keywords
            view_course_result = Course.courses_overview(self)  ## call course_overview methond from course class

        elif len(args) != 2:  ## if the lenth of admin input is not 2
            view_course_result = Course.courses_overview(self)  ## call course_overview methond from course class

        else:
            if args[0] == "TITLE_KEYWORD":  ## if the first element of admin is "TITLE_KEYWORD"
                view_course_result = Course.find_course_by_title_keyword(self, args[
                    1])  # call methond find_course_by_title_keyword

            elif args[0] == "ID":  ## if the first element of admin is "ID"
                view_course_result = Course.find_course_by_id(self, args[1])  ###call methond find_course_by_id

            elif args[0] == "INSTRUCTOR_ID":  ## if the first element of admin is "INSTRUCTOR_ID"
                view_course_result = Course.find_course_by_instructor_id(self, args[
                    1])  #####call methond find_course_by_instructor_id

            else:
                view_course_result = Course.courses_overview(
                    self)  ## if the  admin's input information does not match any words,call course overview methond and print out result
            print(view_course_result)

    def view_users(self):  ## this methond is used to view total number of users
        student_lst = []
        instructor_lst = []
        admin_lst = []

        with open('./data/result/user_student.txt',
                  'r') as view_student_f:  ## add every lines from student result file to list for check lenth
            for line in view_student_f:
                student_lst.append(line)
        with open('./data/result/user_instructor.txt',
                  'r') as view_instructor_f:  ## add every lines from instructor result file to list for check lenth
            for line in view_instructor_f:
                instructor_lst.append(line)

        with open('./data/result/user_admin.txt',
                  'r') as view_admin_f:  ## add every lines from admin result file to list for check lenth
            for line in view_admin_f:
                admin_lst.append(line)

        print('STUDENT NUMBER:{}'.format(
            len(student_lst)))  ## total number of students will be the lenth of student_lst and print out
        print('INSTRUCTOR NUMBER:{}'.format(
            len(instructor_lst)))  ## total number of instructor will be the lenth of instructor_lst and print out
        print('ADMIN NUMBER:{}'.format(
            len(admin_lst)))  ## total number of admin will be the lenth of admin_lst and print out

    def view_reviews(self, args=[]):  ## this methond is used for admin view reviews
        if args == '':  ## if admin doesn't enter any keywords
            view_reviews_result = Review.reviews_overview(self)  ## call reviews_overview methond from review class
            print(view_reviews_result)
        elif len(args) != 2:  ## if the lenth of admin input is not 2
            view_reviews_result = Review.reviews_overview(self)  ## call reviews_overview methond from review class
            print(view_reviews_result)
        else:
            if args[0] == "TITLE_KEYWORD":  ## if the first element of admin is "TITLE_KEYWORD"
                view_reviews_result = Review.find_review_by_keywords(self, args[
                    1])  # call methond find_review_by_keywords from review class
                print(view_reviews_result)
            elif args[0] == "ID":  ## if the first element of admin is "ID"
                view_reviews_result = Review.find_review_by_id(self, args[
                    1])  ###call methond find_review_by_id from review class
                print(view_reviews_result)
            elif args[0] == "COURSE_ID":  ## if the first element of admin is "COURSE_ID"
                view_reviews_result = Review.find_review_by_course_id(self, args[1])
                print(view_reviews_result)  #####call methond find_review_by_course_id from review class

            else:
                view_reviews_result = Review.reviews_overview(
                    self)  ## if the  admin's input information does not match any words
                print(view_reviews_result)  ## call reviews_overview methond from review class

    def __str__(self):
        User.__str__(self)



