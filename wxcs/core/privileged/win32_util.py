"""Change local time."""
import sys
from ctypes import Structure, windll, pointer
from ctypes.wintypes import WORD
from datetime import datetime

SetLocalTime = windll.kernel32.SetLocalTime
ShellExecuteW = windll.shell32.ShellExecuteW
IsUserAnAdmin = windll.shell32.IsUserAnAdmin


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


def _win_is_admin():
    """Win32 - Check if exec as admin."""
    try:
        return IsUserAnAdmin()
    except Exception:
        return False


def _win_gen_systime(time_str):
    """Generate and return win32 systime."""
    dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    dt_tuple = dt.timetuple()

    st = SYSTEMTIME()
    st.wYear = dt_tuple.tm_year
    st.wMonth = dt_tuple.tm_mon
    st.wDayOfWeek = (dt_tuple.tm_wday + 1) % 7
    st.wDay = dt_tuple.tm_mday
    st.wHour = dt_tuple.tm_hour
    st.wMinute = dt_tuple.tm_min
    st.wSecond = dt_tuple.tm_sec
    st.wMilliseconds = 0
    return st


def _win_set_time(time_str):
    """Set win32 time to desired time."""
    try:
        if _win_is_admin():
            systime = _win_gen_systime(time_str)
            SetLocalTime(pointer(systime))
            return True
        else:
            lp_params = f'"{__file__}" "{time_str}"'
            ret = ShellExecuteW(None, 'runas', sys.executable, lp_params, None, 1)
            return ret == 42  # 42 - success, 5 - fail
    except Exception:
        return False


if __name__ == '__main__':
    _win_set_time(sys.argv[1])
