import datetime

def format_date_from_iso(isodate, format = "%d/%m/%Y %H:%M"):
    return datetime.datetime.fromisoformat(isodate).strftime(format)