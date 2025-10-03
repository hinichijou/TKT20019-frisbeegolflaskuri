import datetime


class Singleton:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def __repr__(self):
        return "I am a Singleton. This is a method that supresses too few public methods linter error."


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
