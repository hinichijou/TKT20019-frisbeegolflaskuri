from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def link_with_text(l, t):
    return Markup(f"<a href='{l}'> {t} </a>")

def return_to_index_link():
    return link_with_text("/", get_localization(LocalizationKeys.return_to_index_button))

def edit_round_link(round_id):
    return link_with_text(f"/edit_round/{round_id}", get_localization(LocalizationKeys.modify_button))

def delete_round_link(round_id):
    return link_with_text(f"/delete_round/{round_id}", get_localization(LocalizationKeys.delete_button))