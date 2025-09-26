from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization
from constants import constants


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def submit_button_with_text(t):
    return Markup(f"<input type='submit' value='{t}' />")

def user_input(type, name, minlength, maxlength, required):
    return Markup(f"<input \
                        type='{type}' \
                        name='{name}' \
                        required='{required}' \
                        minlength='{minlength}' \
                        maxlength='{maxlength}' \
                    />")

def user_input_with_header(headerkey, type, name, minlength, maxlength, required):
    return Markup(f"{get_localization(headerkey)} <br />{user_input(type, name, minlength, maxlength, required)}")

def hidden_input(n, v):
    return Markup(f"<input type='hidden' name='{n}' value='{v}' />")

def link_with_text(l, t):
    return Markup(f"<a href='{l}'> {t} </a>")

def account_name_input():
     return user_input_with_header(LocalizationKeys.account_name_header, \
                                    "text", \
                                    "username", \
                                    constants.username_minlength, \
                                    constants.username_maxlength, \
                                    True
                                )

def base_password_input(headerkey, name):
     return user_input_with_header(headerkey, \
                                    "password", \
                                    name, \
                                    constants.password_minlength, \
                                    constants.password_maxlength, \
                                    True
                                )

def password_input():
     return base_password_input(LocalizationKeys.password_header, "password")

def repeat_password_input():
     return base_password_input(LocalizationKeys.repeat_password_header, "repeat_password")

def return_to_index_link():
    return link_with_text("/", get_localization(LocalizationKeys.return_to_index_button))

def edit_round_link(round_id):
    return link_with_text(f"/edit_round/{round_id}", get_localization(LocalizationKeys.modify_button))

def delete_round_link(round_id):
    return link_with_text(f"/delete_round/{round_id}", get_localization(LocalizationKeys.delete_button))

def new_course_link():
    return link_with_text(f"/new_course", get_localization(LocalizationKeys.create_course_button))

def show_courses_link():
    return link_with_text(f"/show_courses", get_localization(LocalizationKeys.browse_courses_button))

def new_round_link():
    return link_with_text(f"/new_round", get_localization(LocalizationKeys.create_round_button))

def find_round_link():
    return link_with_text(f"/find_round", get_localization(LocalizationKeys.find_round_button))

def login_link():
    return link_with_text(f"/login", get_localization(LocalizationKeys.log_in_button))

def logout_link():
    return link_with_text(f"/logout", get_localization(LocalizationKeys.log_out_button))

def register_link():
    return link_with_text(f"/register", get_localization(LocalizationKeys.register_button))

def user_link(user_id, username):
    return link_with_text(f"/user/{user_id}", username)

def course_link(course_id, text):
    return link_with_text(f"/course/{course_id}", text)

def round_link(round_id, text):
    return link_with_text(f"/round/{round_id}", text)

def round_list_item(round):
    return Markup(f"<li><a href='/round/{round["id"]}'>\
                    { get_localization(LocalizationKeys.round_item_start) } {round["start_time"]} \
                    { get_localization(LocalizationKeys.round_item_place) } {round["coursename"]}, \
                    { get_localization(LocalizationKeys.round_item_creator) } {round["username"]}, \
                    { get_localization(LocalizationKeys.round_item_players) } {round["num_participating"]} / {round["num_players"]}\
                </a></li>")