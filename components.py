from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def link_with_text(t):
    return Markup(f"<a href='/'> {t} </a>")

def return_to_index_link():
        return link_with_text(get_localization(LocalizationKeys.return_to_index_button))