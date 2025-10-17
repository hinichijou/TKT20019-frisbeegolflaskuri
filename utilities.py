import datetime

from enums import ResultCategory, InputCategory
from localizationkeys import LocalizationKeys
from localization import get_localization
from constants import constants


def format_date_from_iso(isodate, format_="%d/%m/%Y %H:%M"):
    return datetime.datetime.fromisoformat(isodate).strftime(format_)


# If you use an empty collection as default value in python the same default
# will be modified between multiple function calls if the collection is returned from the function.
# The options are to suppress the linter error or use None combined with this as default.
def use_default_if_list_none(list_, default=None):
    if list_ is None:
        return [] if default is None else default

    return list_


def get_page_limit_and_offset(page, page_size):
    limit = page_size
    offset = page_size * (page - 1)
    return limit, offset


def get_type_for_result(result, par):
    if result <= par - 2:
        return ResultCategory.EAGLE
    if result == par - 1:
        return ResultCategory.BIRDIE
    if result == par:
        return ResultCategory.PAR
    if result == par + 1:
        return ResultCategory.BOGEY
    if result >= par + 2:
        return ResultCategory.DOUBLEBOGEY

    return ResultCategory.DEFAULT


def get_round_over_under_string(results, hole_data):
    result = 0
    for key in hole_data.keys():
        intkey = int(key)
        if intkey in results:
            result += results[intkey]["result"] - int(hole_data[key]["par"])

    return str(result) if result <= 0 else "+" + str(result)


def create_where_condition(params, sql_for_param_func):
    where = ""

    for i, p in enumerate(params):
        if i == 0:
            where += "WHERE " + sql_for_param_func(p) + " "
        else:
            where += "AND " + sql_for_param_func(p) + " "

    return where


def get_allowed_characters_message(input_category, localizationkey):
    match input_category:
        case InputCategory.USERNAME:
            return get_localization(localizationkey).format((" ").join(constants.name_allowed_special_characters))
        case InputCategory.COURSENAME:
            return get_localization(localizationkey).format((" ").join(constants.name_allowed_special_characters))
        case _:
            return ""
