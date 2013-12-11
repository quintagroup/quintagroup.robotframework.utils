import datetime
from dateutil import tz, relativedelta


def get_current_time(time_zone, formatting="%Y-%m-%d %I:%M %p",
                     timedelta=None):
    """
    returns current time according to the given timezone. For more details see
    http://docs.python.org/library/datetime.html

    >>> get_current_time('Europe/London') and True
    True

    """
    local_tz = tz.tzlocal()
    site_tz = tz.gettz(time_zone)
    localtime = datetime.datetime.now()
    if timedelta:
        timedelta = dict([(i.split("=")[0], int(i.split("=")[1]))
                          for i in timedelta.split(",")])
        localtime += relativedelta.relativedelta(**timedelta)
    localtime = localtime.replace(tzinfo=local_tz)
    site_time = localtime.astimezone(site_tz)
    srt_time = site_time.strftime(formatting)
    return srt_time
