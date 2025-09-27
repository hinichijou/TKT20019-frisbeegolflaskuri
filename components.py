from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization
from constants import constants


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def argsToParamString(*args):
    s = ""
    for v in args:
        s += v

    return s

def kwargsToParamString(**kwargs):
    s = ""
    for key, value in kwargs.items():
        s += f"{key}={value} "

    return s

def submit_button_with_text(t):
    return Markup(f"<input type='submit' value='{t}' />")

def user_input(type, name, *args, **kwargs):
    return Markup(f"<input \
                        type='{type}' \
                        name='{name}' \
                        {argsToParamString(*args)} \
                        {kwargsToParamString(**kwargs)} \
                    />")

def user_input_with_header(headerkey, type, name, *args, **kwargs):
    return Markup(f"{get_localization(headerkey)} <br />{user_input(type, name, *args, **kwargs)}")

def select(name, options, *args, **kwargs):
    return Markup(f"<select  \
                        name='{name}' \
                        {argsToParamString(*args)} \
                        {kwargsToParamString(**kwargs)} \
                    > \
                        {options} \
                    </select>")

def select_with_header(headerkey, name, options, *args, **kwargs):
    return Markup(f"{get_localization(headerkey)} <br />{select(name, options, *args, **kwargs)}")

def text_input(headerkey, type, name, minlength, maxlength, *args, **kwargs):
    return user_input_with_header(headerkey,
                                    type,
                                    name,
                                    *args,
                                    minlength=minlength,
                                    maxlength=maxlength,
                                    **kwargs
                                )

def number_input(headerkey, name, min, max, *args, **kwargs):
     oninput = """oninput="this.value = Math.min('""" + str(max) + "', Math.max(this.value|0, '" + str(min) + """'))\""""

     return user_input_with_header(headerkey,
                                    "number",
                                    name,
                                    oninput,
                                    *args,
                                    min=min,
                                    max=max,
                                    **kwargs
                                )

def date_input(headerkey, name, *args, **kwargs):
     return user_input_with_header(headerkey,
                                    "datetime-local",
                                    name,
                                    *args,
                                    **kwargs
                                )

def inert_select(headerkey, name, selection):
    options = f"<option value='{ selection[0] },{ selection[1] }'>{ get_localization(selection[1]) }</option>"

    return select_with_header(headerkey, name, options, "required", "inert")

def hidden_input(n, v):
    return user_input('hidden', n, value=v)

def inert_text_input(headerkey, name, value):
    return user_input_with_header(headerkey, "text", name, "inert", value=value)

def link_with_text(l, t):
    return Markup(f"<a href='{l}'> {t} </a>")

def account_name_input():
     return text_input(LocalizationKeys.account_name_header,
                        "text",
                        "username",
                        constants.username_minlength,
                        constants.username_maxlength,
                        "required"
                    )

def base_password_input(headerkey, name):
     return text_input(headerkey,
                        "password",
                        name,
                        constants.password_minlength,
                        constants.password_maxlength,
                        "required"
                    )

def password_input():
     return base_password_input(LocalizationKeys.password_header, "password")

def repeat_password_input():
     return base_password_input(LocalizationKeys.repeat_password_header, "repeat_password")

def course_name_input():
     return text_input(LocalizationKeys.course_name_header,
                        "text",
                        "coursename",
                        constants.coursename_minlength,
                        constants.coursename_maxlength,
                        "required"
                    )

def amount_players_input():
     return number_input(LocalizationKeys.amount_players_header,
                            "num_players",
                            constants.round_min_players,
                            constants.round_max_players,
                            "required",
                            value = constants.round_min_players
                        )

def course_holes_input():
     return number_input(LocalizationKeys.course_holes_header,
                            "num_holes",
                            constants.course_holes_min,
                            constants.course_holes_max,
                            "required",
                            value = constants.course_holes_default
                        )

def start_date_input(value):
     return date_input(LocalizationKeys.start_time_header, "start_time", "required", value=value)


def course_select(courses, *args):
    options = f"<option hidden selected value=''>{ get_localization(LocalizationKeys.course_select_default) }</option>"

    for course in courses:
        options += f"<option value='{ course["id"] }'>{ course["coursename"] }</option>"

    return select_with_header(LocalizationKeys.select_course_header, "course_select", options, *args)

def select_from_option_tuple(name, headerkey, defaultkey, selection, *args):
    options = f"<option hidden selected value=''>{ get_localization(defaultkey) }</option>"

    for s in selection:
        options += f"<option value='{ s[0] },{ s[1] }'>{ get_localization(s[1]) }</option>"

    return select_with_header(headerkey, name, options, *args)

def course_type_select(ctypes, *args):
    return select_from_option_tuple("type_select", LocalizationKeys.course_type_header, LocalizationKeys.course_type_default, ctypes, *args)

def course_difficulty_select(cds, *args):
    return select_from_option_tuple("difficulty_select", LocalizationKeys.course_difficulty_header, LocalizationKeys.course_diff_default, cds, *args)

def par_input(index):
     return number_input(LocalizationKeys.par_header, \
                            f"par_{index}", \
                            constants.hole_par_min, \
                            constants.hole_par_max, \
                            "required",
                            value = constants.hole_par_default
                        )

def length_input(index):
     return number_input(LocalizationKeys.hole_length_header, \
                            f"length_{index}", \
                            constants.hole_length_min, \
                            constants.hole_length_max, \
                            "required",
                            value = constants.hole_length_default
                        )

def course_difficulty_inert_select(selection):
    return inert_select(LocalizationKeys.course_difficulty_header, "difficulty_select", selection)

def course_type_inert_select(selection):
    return inert_select(LocalizationKeys.course_type_header, "type_select", selection)

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
    return Markup(f"<div class='round_item'>\
                    <a href='/round/{round["id"]}' class='nounderline'>\
                        { get_localization(LocalizationKeys.round_item_start) } {round["start_time"]}<br /> \
                        { get_localization(LocalizationKeys.round_item_place) } {round["coursename"]}<br /> \
                        { get_localization(LocalizationKeys.round_item_creator) } {round["username"]}<br /> \
                        { get_localization(LocalizationKeys.round_item_players) } {round["num_participating"]} / {round["num_players"]}<br />\
                    </a>\
                </div>")