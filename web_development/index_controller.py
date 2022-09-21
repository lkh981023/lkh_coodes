"""name: Kehan Liu
start date: 2022.05.19
Last modified date:  2022.06.09
----------------
def index(): this method is used to check the class variable current_login_user to see if there is any logged user then
pass the user role to context
----------------

"""

from flask import render_template, Blueprint
from model.user import User
from model.user_admin import Admin
user = User()
user_admin = Admin()
index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    context = {} ## initialize variable as empty dict
    if User.current_login_user: # check the class variable User.current_login_user
        context['current_user_role'] = User.current_login_user.role ## pass the current login user role to context


    if not user.check_username_exist('admin'): ## if the username admin not in the file
        user_admin.register_admin() ## register admin manually
        print(user_admin.register_admin())


    return render_template("01index.html", **context)


    # check the class variable User.current_login_user

    # manually register an admin account when open index page
