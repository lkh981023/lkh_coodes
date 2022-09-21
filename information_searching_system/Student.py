
"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: This function is used to check user's input message.
"""


from User import User
from Review import Review
from Course import Course


class Student(User):
    def __init__(self, _id=-1, username='', password='', user_title='', user_image_50x50='', user_initials='',
                 review_id=''):
        User.__init__(self, _id, username, password)

        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    def view_courses(self, args=[]): ## this methond is used for user student view courses

        with open('./data/result/user_student.txt', 'r') as student_view_file:
            lst = []
            for line in student_view_file:
                line = line.replace('\n', '').split(';;;')
                lst.append(line) ## open file and reformat lines, then append line in list
        for item in lst: ## using for loop to iterate the element list
            if self.id == item[0]: ## if the student id is same with the first item(exact search)
                student_rev_id = item[-1]  ## assgin the student_rev_id with the last element of item
                break

        student_revi = Review.find_review_by_id(self, student_rev_id)  ## call methond find_review_by_id from class review to get course id

        student_course = Course.find_course_by_id(self, student_revi.course_id) ## call methond find_course_by_id from course class to get student course
        print(student_course) ## print course info belongs to this user student

    def view_reviews(self, args=[]):
        revi_lst = []
        with open('./data/result/user_student.txt', 'r') as student_view_file:
            for line in student_view_file:
                line = line.replace('\n', '').split(';;;')
                revi_lst.append(line) ## open file and reformat lines, then append line in list
            for item in revi_lst:  ## using for loop to iterate the element in list
                if self.id == item[0]: ## if student id is same with the first element
                    student_rev_id = item[-1]  ## assgin the student_rev_id with the last element of item
                    break
        student_revi = Review.find_review_by_id(self, student_rev_id)  ## call methond from review class to get student review
        print(student_revi) ## print out

    def __str__(self):
        return '{};;;{};;;{};;;{};;;{};;;{};;;{}'.format(self.id, self.username
                                                         , self.password
                                                         , self.user_title, self.user_image_50x50,
                                                         self.user_initials
                                                         , self.review_id)  ## reformat the print out string



