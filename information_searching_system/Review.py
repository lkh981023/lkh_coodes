"""
Name: kehan liu
Student ID:32281943
Start Date:2022.04.18
Last modified date:2022.05.06
Description: This module is design for user view reviews.
------------------------------
def find_review_by_id()

def find_review_by_keywords()
def reviews_overview()

"""


class Review:

    def __init__(self, _id=-1, content='', rating=-1.0, course_id=-1):
        self.id = _id
        self.content = content
        self.rating = rating
        self.course_id = course_id

    def find_review_by_id(self, review_id): ## this methond is used for find reviews by review id

        review_matched_result = []
        with open('./data/result/course_review.txt', 'r') as ck_file:
            for line in ck_file:
                line = line.replace('\n', '').split(';;;')
                review_matched_result.append(line) ## open file and reformat lines, then append line in list
        for item in review_matched_result: ## using for loop to iterate the element
            if review_id == item[0]: ## if the review id is same with the first item
                return Review(item[0], item[1], item[2], item[3]) ## return object of class review


    def find_review_by_keywords(self, keyword): ## this methond is used for find reviews by content keyword
        rev_keyword_ck = []
        rev_ck_result = []
        keyword_lst = []
        with open('./data/result/course_review.txt', 'r') as ck_rev_keyword_f:
            for line in ck_rev_keyword_f:
                line = line.replace('\n', '').split(';;;')
                rev_keyword_ck.append(line) ## open file and reformat lines, then append line in list
            for item in rev_keyword_ck:
                if keyword in item[1]: ## if the content key is in the  second items(fuzzy search)
                    keyword_lst.append(item) ## append the item to list
            for each in keyword_lst:
                rev_ck_result.append(Review(each[0], each[1], each[2], each[3])) ## append to the result list and return
            return rev_ck_result




    def find_review_by_course_id(self, course_id):
        ck_list = []
        ck_id_result = []
        course_id_lst = []
        with open('./data/result/course_review.txt', 'r') as check_rev_by_id_f:
            for line in check_rev_by_id_f:
                line = line.replace('\n', '').split(';;;')
                ck_list.append(line)## open file and reformat lines, then append line in list
        for item in ck_list:
            if course_id == item[3]: ## using for loop to iterate the item in list, check if the course id is same with the third element in item(exact search)
                course_id_lst.append(item) ## append the match item to list
        for each in course_id_lst: ## using for loop to iterate the elemnt in course_id_lst
            ck_id_result.append(Review(each[0], each[1], each[2], each[3]))
        return ck_id_result ## append to the result list and return

    def reviews_overview(self):
        with open('./data/result/course_review.txt', 'r') as rev_overview_file:
            rev_overview = rev_overview_file.readlines()
        return 'Total number of review: {}'.format(len(rev_overview)) ## open file and check lenth of lines of the file, return string contain total number of reviews

    def __str__(self):
        return 'rev_id:{},rev_content:{},rev_rating:{},rev_course_id:{}'.format(self.id, self.content
                                                                                , self.rating,self.course_id)   ## reformat string and print out


