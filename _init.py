import time
from datetime import datetime
import pyperclip as pc
from selenium.webdriver.common.keys import Keys

class CommonFucntion():
    def str_from_to(self, _str, _from, _to):
        _tmp_str = _str.split(_from)[1]
        _tmp_str = _tmp_str.split(_to)[0]
        return _tmp_str
