from markupsafe import Markup
from localizationkeys import LocalizationKeys
from localization import get_localization


# A test for creating and sharing some basic components between templates. Could build a library of basic components and call them with functions from the templates
# Other methods that Jinja seems to offer: template inheritance, include statement, macros

def get_return_to_index_button():
        return Markup(f"<a href='/'> {get_localization(LocalizationKeys.return_to_index_button)} </a>")