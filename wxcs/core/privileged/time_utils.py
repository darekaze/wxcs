"""Change local time."""
import sys
from datetime import datetime

CLOCK_REALTIME = 0


def _win_set_time(time_str):
    """Set win32 time to desired time."""
    from ctypes import Structure, windll, pointer
    from ctypes.wintypes import WORD

    class SYSTEMTIME(Structure):
        """Win32 systime."""

        _fields_ = [
            ('wYear', WORD),
            ('wMonth', WORD),
            ('wDayOfWeek', WORD),
            ('wDay', WORD),
            ('wHour', WORD),
            ('wMinute', WORD),
            ('wSecond', WORD),
            ('wMilliseconds', WORD)]

    def is_admin():
        """Win32 - Check if exec as admin."""
        try:
            return windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def gen_systime(time_str):
        """Generate and return win32 systime."""
        dt = datetime.fromisoformat(time_str).timetuple()

        st = SYSTEMTIME()
        st.wYear = dt.tm_year
        st.wMonth = dt.tm_mon
        st.wDayOfWeek = (dt.tm_wday + 1) % 7
        st.wDay = dt.tm_mday
        st.wHour = dt.tm_hour
        st.wMinute = dt.tm_min
        st.wSecond = dt.tm_sec
        st.wMilliseconds = 0
        return st

    try:
        if is_admin():
            systime = gen_systime(time_str)
            windll.kernel32.SetLocalTime(pointer(systime))
            return True
        else:
            lp_params = f'"{__file__}" "{time_str}"'
            ret = windll.shell32.ShellExecuteW(None, 'runas', sys.executable, lp_params, None, 1)
            return ret == 42  # 42 - success, 5 - fail
    except Exception:
        return False


def _linux_set_time(time_str):
    """Generate and return linux systime.

    Ref: http://linux.die.net/man/3/clock_settime
    """
    from time import mktime
    from ctypes import Structure, c_long, byref, CDLL
    from ctypes.util import find_library

    class Timespec(Structure):
        """Linux systime."""

        _fields_ = [
            ('tv_sec', c_long),
            ('tv_nsec', c_long)]

    librt = CDLL(find_library('rt'))

    try:
        ts = Timespec()
        dt_tuple = datetime.fromisoformat(time_str).timetuple()
        ts.tv_sec = int(mktime(dt_tuple))
        ts.tv_nsec = 0

        librt.clock_settime(CLOCK_REALTIME, byref(ts))
        return True
    except Exception:
        return False


def set_time(time_str):
    """Set local time based on OS."""
    if sys.platform == 'win32':
        ret = _win_set_time(time_str)
    elif sys.platform.startswith('linux'):
        ret = _linux_set_time(time_str)
    else:
        ret = False
    return ret


if __name__ == '__main__':
    set_time(sys.argv[1])
