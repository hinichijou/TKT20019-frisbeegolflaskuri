import datetime

class Singleton:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

def format_date_from_iso(isodate, format = "%d/%m/%Y %H:%M"):
    return datetime.datetime.fromisoformat(isodate).strftime(format)