from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def submit_button_with_text(t):
    return Markup(f"<input type='submit' value='{t}' />")

def hidden_input(n, v):
    return Markup(f"<input type='hidden' name='{n}' value='{v}' />")

def link_with_text(l, t):
    return Markup(f"<a href='{l}'> {t} </a>")

def return_to_index_link():
    return link_with_text("/", get_localization(LocalizationKeys.return_to_index_button))

def edit_round_link(round_id):
    return link_with_text(f"/edit_round/{round_id}", get_localization(LocalizationKeys.modify_button))

def delete_round_link(round_id):
    return link_with_text(f"/delete_round/{round_id}", get_localization(LocalizationKeys.delete_button))

def user_link(user_id, username):
    return link_with_text(f"/user/{user_id}", username)

def course_link(course_id, text):
    return link_with_text(f"/course/{course_id}", text)

def round_link(round_id, text):
    return link_with_text(f"/round/{round_id}", text)