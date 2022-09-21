"""name: Kehan Liu
start date: 2022.05.19
Last modified date:  2022.06.09
----------------
def login(): return 00login.html page
----------------
def login_post():this function is used for process user login
----------------
def logout(): this function is used for process user logout
----------------
def generate_user(login_user_str): this function is used for generate login user infomation
----------------
def register(): return register page
----------------
def register_post(): this function is used for process user register
--------------------
def student_list(): this function is used for exihibit student info on web page by call student class method
-------------------
def student_info(): this function is used for exihibit student detail info on web page by call student class method
-------------------
def student_delete(): this function is used for admin  delete student info by call student class method
"""

from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


@user_page.route("/login")
def login():
    return render_template("00login.html")


@user_page.route("/login", methods=["POST"])
def login_post():
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else "" ##get username and password from request values
    if not model_user.validate_username(username): ## call methond validate username from user class
        return render_err_result(msg="plz check your username format!(˘̩̩̩ε˘̩ƪ)") ## return error message if the username is invalid for requirement
    if not model_user.validate_password(password): ## call method validate password from user class
        return render_err_result(msg='plz check your password!(˘̩̩̩ε˘̩ƪ)') ## return error message if the password is invalid for requirement

    login_result, login_user_infor = model_user.authenticate_user(username, password) ##if meet requirement, pass the login result and user infor to the authenticate user method
    # print(username, password)
    if login_result: ## if login result is true
        users_obj = generate_user(login_user_infor) ## pass the user infor to the generetate user method and assign the variable to user object
        User.current_login_user = users_obj ## assign user to the class variable
        # print(User.current_login_user)
        return render_result(msg="user login successfully ಠ‿ಠ") ## return login successful message if user login input is valid
    else:
        return render_err_result(msg="pleases check your username and password (˘̩̩̩ε˘̩ƪ)") ## if not, return error message

@user_page.route("/logout")
def logout():
    User.current_login_user  = None ## reset class variable to none
    return render_template("01index.html") ## return index page

def generate_user(login_user_str):

    login_user = None  # a User object
    users_inf = login_user_str.strip().split(';;;') ## transfer the login_user_str to list
    if users_inf[4] == 'admin': ## if role is admin
        login_user = Admin(users_inf[0], users_inf[1], users_inf[2], users_inf[3], users_inf[4]) ## covert to user_str to admin object
    elif users_inf[4] == 'instructor':## if role is instructor
        login_user = Instructor(users_inf[0], users_inf[1], users_inf[2], users_inf[3], users_inf[4], users_inf[5],
                                users_inf[6], users_inf[7], users_inf[8]) ## covert to user_str to instructor object
    elif users_inf[4] == 'student':## if role is stduent
        login_user = Student(users_inf[0], users_inf[1], users_inf[2], users_inf[3], users_inf[4],users_inf[5]) ## covert to user_str to student object

    return login_user

# use @user_page.route("") for each page url

@user_page.route("/register")
def register():
    return render_template("00register.html") ## return register page

@user_page.route("/register", methods=["POST"])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else ""
    email = req["email"] if "email" in req else ""
    register_time = req["register_time"] if "register_time" in req else ""
    role = req["role"] if "role" in req else "" ## get username, password, email, register time and role from request values
    if model_user.validate_username(username) and model_user.validate_password(password) and \
            model_user.validate_email(email) and model_user.register_user(username, password, email, register_time, role): ## call valide methonds from user clss, if result all true
        return render_result(msg="❤️USER REGISTER SUCCESSFULLY!❤️") ## return register successful message
    else:
        return render_result(msg="REGISTER FAILED!(ಥ_ಥ)") ## if not, return fialed message


@user_page.route("/student-list")
def student_list():
    context = {} ## intialize variable
    if User.current_login_user:
        req = request.values ## get info from request values
        page = req['page'] if "page" in req else 1
        one_page_student_list, total_pages, total_num = model_student.get_students_by_page(int(page))
        page_num_list = model_course.generate_page_num_list(page, total_pages)  # get values for page_num_list
        if not one_page_student_list:
            one_page_student_list = []  # check one_page_stduent_list, make sure this variable not be None, if None, assign it to []

        context['one_page_student_list'] = one_page_student_list
        context['total_pages'] = total_num
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num
        context['current_user_role'] = User.current_login_user.role # add "current_user_role" to context
    else:
        return redirect(url_for("index_page.index"))
    return render_template("10student_list.html", **context)

@user_page.route("/student-info")
def student_info():
    context = {}
    req = request.values ## initialize variable
    student_id = req['id'] if "id" in req else ""
    if student_id == "": ## if student is not exist
        student_id = User.current_login_user.uid ## return a new student
    student = model_student.get_student_by_id(str(student_id))
    context['id'] = student.uid
    context['username'] = student.username
    context['password'] = student.password
    context['email'] = student.email
    context['current_user_role'] = User.current_login_user.role  ## set all instance variables with default values
    return render_template("11student_info.html", **context)

@user_page.route("/student-delete")
def student_delete():
    req = request.values
    student_id = req['id'] if 'id' in req else -1
    print('student_delete:', student_id) ## get the id that will be deleted
    if student_id == -1:
        return render_err_result(msg='student_cannot_find') ## if cannot find id, return error message
    delete_result = model_student.delete_student_by_id(int(student_id)) ## if find, call the method in student class
    print('student delete:', delete_result)
    if delete_result:
        return redirect(url_for('user_page.student_list')) ## if delete successfully, return student_list page
    else:
        return redirect(url_for('index_page.index')) ## if not, return index page



