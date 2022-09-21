"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: this module is design for the instructor login system and view their own information
-------------------------------
def view_course()
design for instructor view their courses
only the first 10 courses will be printed
if the instructor teach more than 10 curses
----------------------------
def view_reviews()
design for instructor view their courses reviews
only the first 10 courses reviews will be printed if
this instructor teach more than 10 courses

"""

from User import User
from Course import Course
from Review import Review


class Instructor(User):

    def __init__(self, _id=-1, username='', password='', display_name='', job_title='', image_100x100='',
                 course_id_list=[]): ##transit the instructor user information from user class
        self.id = _id
        self.username = username
        self.password = password
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id_list = course_id_list

    def view_course(self, args=[]): ## this methond is used for user instructor to view course
        course_taught_by_instructor = Course.find_course_by_instructor_id(self, self.id) ## match the instructor course by using the methond find_course_by_instructor_id from course class
        if len(course_taught_by_instructor) >= 10:
            course_taught_by_instructor = course_taught_by_instructor[0:10] ## if the instructor has taught more than 10 courses, only print out the first 10 courses
        for item in course_taught_by_instructor:
            print(item) ## print the course information that taught by the user

    def view_reviews(self, args=[]): ## this methond is used for instructors view reviews
        course_taught_by_instructor = Course.find_course_by_instructor_id(self, self.id) ## to check the course reviews from the corse that taught by this instructor, transit the instrucor
        course_rev = []                                                                  ##id to the methond find_course_by_instructor_id from course class
        for item in course_taught_by_instructor: ## since the methond return a list, so use for loop to iterate the item in list
            rev_list = Review.find_review_by_course_id(self, item.course_id) ## using methond find_review_by_course_id from review class to get course review
            course_rev = course_rev + rev_list
        if len(course_rev) >= 10: ## if the instructor is teaching more than 10 courses, only print out first 10 courses
            course_rev = course_rev[0:10]
        for each in course_rev:
            print(each) ## print course reviews taught by this user instructor

    def __str__(self): ## reformat the information and print out

        course_id = '-'.join(self.course_id_list) ## since the instructor may not only teach one course, using"-" to seprate different course id

        return '{};;;{};;;{};;;{};;;{};;;{};;;{}'.format(self.id,
                                                         self.username, self.password, self.display_name,
                                                         self.job_title,
                                                         self.image_100x100, course_id)


