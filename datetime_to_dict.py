import datetime


def get_datetime_as_dict(datetime: datetime.datetime):
    if datetime is None:
        return None
    dictionary = {'year': datetime.year,
                  'month': datetime.month,
                  'day': datetime.day,
                  'hour': datetime.hour,
                  'minute': datetime.minute,
                  'second': datetime.second,
                  'microsecond': datetime.microsecond}
    return dictionary
