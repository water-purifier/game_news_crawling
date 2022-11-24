import time,re,os.path
from datetime import datetime
import pyperclip as pc

class CommonFucntion():
    def str_from_to(self, _str, _from, _to):
        _tmp_str = _str.split(_from)[1]
        _tmp_str = _tmp_str.split(_to)[0]
        return _tmp_str

    def remove_spe_char(self,_strr):
        newStr = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", _strr)
        return newStr

    def remove_emojis(self, data):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoj, '', data)


    def get_pid(self,_url):
        xs = re.findall("/\d+-\d+/", _url)
        for x in xs:
            return x.replace('/', '')
        return '0000'

    def json_exists(self,file_path_name):
        if os.path.isfile(file_path_name):
            return True
        else:
            return False