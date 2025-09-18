from enum import StrEnum, auto

#The idea would be that we could use these keys in the code with dot notation which then map into localizations that are stored in a json file as key-value pairs. A different file could be loaded for a different language
#The usefulness seems to be limited as
class LocalizationKeys(StrEnum):
    str_no_courses_found = auto()

def get_localization_key(s):
    try:
        key = LocalizationKeys(s)
    except ValueError:
        print(f"Virhe: lokalisaatioavainta {s} ei ole määritetty.")
        return s
    return key