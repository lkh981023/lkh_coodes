
"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: This module is design for users view course
---------------------------------------
def find_course_by_title_keyword()
design for admin view course while type some keyword
---------------------------
def find_course_by_id()
search course with its course id
----------------------------------
def find_course_by_instructor_id()
search the course taught by the instructor while using the instructor id to match
------------------------------------
def courses_overview()
print out total number of courses
"""

class Course:
    def __init__(self, course_id=-1, course_title='', course_image_100x100='', course_headline='',
                 course_num_subscribers=-1, course_avg_rating=-1.0, course_content_length=-1.):
        self.course_id = course_id
        self.course_title = course_title
        self.course_image_100x100 = course_image_100x100
        self.course_headline = course_headline
        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating
        self.course_content_length = course_content_length

    def find_course_by_title_keyword(self, keyword): ## this methond is using for find course by keyword
        course_ck_result = []
        result_lst = [] ### initialize the list that will be used
        with open('./data/result/course.txt', 'r') as file_check:
            for line in file_check:
                line = line.replace('\n', '').split(';;;')
                course_ck_result.append(line) ## open the file and read, save every lines message in list
            for item in course_ck_result: ## using for loop to iterate the item in list
                if keyword in item[1].lower(): ## if the second item contain the keyword(fuzzy search)
                    result_lst.append(Course(item[0], item[1], item[2], item[3], item[4],
                                             item[5], item[6])) ## append the item to list

            return result_lst ## return list

    def find_course_by_id(self, course_id):
        match_course_id = []
        with open('./data/result/course.txt', 'r') as check_course_id_f:
            for line in check_course_id_f:
                line = line.replace('\n', '').split(';;;')
                match_course_id.append(line) ## open the file and read, save every lines message in list
        for item in match_course_id: ## using for loop to iterate the item in list
            if course_id == item[0]: ## if the course id is same with the first element in list(Exact search)
                return Course(item[0], item[1], item[2], item[3], item[4],
                                           item[5], item[6]) ## return course object

    def find_course_by_instructor_id(self, instructor_id):
        result_list = []
        instructor_lst = []
        with open('./data/result/user_instructor.txt', 'r') as check_instructor_f:
            for line in check_instructor_f:
                line = line.replace('\n', '').split(';;;')
                instructor_lst.append(line)## open the file and read, save every lines message in list
        for item in instructor_lst:## using for loop to iterate the items in list
            if instructor_id == item[0]:## if the instructor id is same with the first element in list(Exact search)
                matched_course_id = item[-1].replace('-', '') ## reformat the course id which has been saved in file
                for each in matched_course_id:## using for loop to iterate the items in string course id
                    result_list.append(Course.find_course_by_id(self, each)) ## call the methond find course by id to get the object and append to list
                return result_list ## return list

    def courses_overview(self):
        with open('./data/result/course.txt') as overview_file:
            course_overview = overview_file.readlines()
        return 'Total course is {}'.format(len(course_overview)) ## open file and check lenth of lines of the file, return string

    def __str__(self): ## reformat the string contain all object and return
        return '''course_id:{},course_title:{},image{},headline{},num_subscribers{},
                                      avg_rating{},content_length{}'''.format(self.course_id, self.course_title
                                                                              , self.course_image_100x100,
                                                                              self.course_headline,
                                                                              self.course_num_subscribers,
                                                                              self.course_avg_rating,
                                                                              self.course_content_length)





