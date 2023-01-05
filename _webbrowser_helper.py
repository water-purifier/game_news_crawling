import time, logging, os
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from dotenv import load_dotenv

# load Env


## trans
logging.basicConfig(filename='./logs/gamespot_getter_broswer.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

ua = UserAgent()


class MyBrowserHelper(webdriver.Chrome):
    def __init__(self, url, driver_path):
        load_dotenv()

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  # interactive
        self.header = {'User-Agent': ua.chrome}
        self.options = Options()
        #########################################################################
        ## 토끼전용 이미지,js 로딩하지 않음
        self.chrome_prefs = {}
        self.options.experimental_options["prefs"] = self.chrome_prefs
        self.chrome_prefs["profile.default_content_settings"] = {"images": 2}
        self.chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        self.options.add_argument("--disable-javascript")
        ##################################################################################
        self.options.add_argument("--no-sandbox")
        if os.getenv("IS_HEADLESS") == "1":
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("user-datas-dir=./venv/lib/python3.9/site-packages/selenium")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(driver_path, options=self.options)
        self.driver.set_window_size(2560, 1440)
        self.driver.implicitly_wait(1)
        self.driver.get(url)
        self.input_xpath = os.getenv("INPUT_XPATH")
        self.output_xpath = os.getenv("OUTPUT_XPATH")
        self.clear_xpath = os.getenv("CLEAR_XPATH")

    def get_url(self, url):
        self.driver.get(url)
        # 错误提示
        if '错误提示' not in self.driver.page_source:
            return True
        else:
            return False

    def is_there(self, _str):
        if _str in self.driver.page_source:
            return True
        else:
            return False

    def get_element(self, _xpath):
        return self.driver.find_element(By.XPATH, _xpath)

    def get_elements(self, _xpath):
        return self.driver.find_elements(By.XPATH, _xpath)

    def scroll_to_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def set_window_size(self, width, height):
        self.driver.set_window_position(0, 0)
        return self.driver.set_window_size(width, height)

    # element.text 반환
    def get_element_text(self, _xpath):
        try:
            if len(self.driver.find_elements(By.XPATH, _xpath)):
                return self.driver.find_elements(By.XPATH, _xpath)[0].text
            else:
                return ''
        except Exception as e:
            return ''

    # element.get_attribute('src') 등 값 반환,
    # xpath , value ==> src , href 등.
    def get_element_attribute(self, _xpath, value):
        try:
            if len(self.driver.find_elements(By.XPATH, _xpath)):
                return self.driver.find_elements(By.XPATH, _xpath)[0].get_attribute(value)
            else:
                return ''
        except Exception as e:
            return ''

    # elements.text 값 반환 array 형식
    def get_elements_text(self, _xpath):
        _elements = self.driver.find_elements(By.XPATH, _xpath)
        texts = []

        for _element in _elements:
            texts.append(_element.text)
        return texts

    def get_elements_href(self, _xpath):
        _elements = self.driver.find_elements(By.XPATH, _xpath)
        hrefs = []
        for _element in _elements:
            hrefs.append(_element.get_attribute('href'))
        return hrefs

    # 지정 버튼의 xpath를 보내면, 클릭함.
    def click_element(self, _xpath):
        try:
            if len(self.driver.find_elements(By.XPATH, _xpath)):
                self.driver.find_elements(By.XPATH, _xpath)[0].click()
        except Exception as e:
            logging.error(e)

    # section 하위 다수의 img태그를 찾을시 사용됨.
    def get_elements_src_by_css_selector(self, _selector):
        _elements = self.driver.find_elements(By.CSS_SELECTOR, _selector)
        srcs = []
        for _element in _elements:
            srcs.append(_element.get_attribute('src'))
        return srcs

    # s는 string, w: 맥심 크기
    def text_wrap(self, s, w):
        return [s[i:i + w] for i in range(0, len(s), w)]

    # 구글 번역 페이지에서 text, 입력 xpath, 출력 xpath, 그리고 입력창 삭제 버튼의 xpath를 지정
    def paste_trans(self, text):
        input_element = self.get_element(self.input_xpath)
        # Clear Text 버튼이 있을시만 클릭, output_xpath 내용이 있을때 === Clear Text Button 있을때
        if len(self.driver.find_elements(By.XPATH, self.output_xpath)):
            self.click_element(self.clear_xpath)
        # \t 가 있으면, tab 으로 여겨서, 붙여넣기 안됨. 그리하여 strip(c# 의 trim비슷)하여, \t \n , . 등을 없앨수 있음.
        text = text.replace('\t', '')
        input_element.send_keys(text)
        split_trans = ""
        count = 0
        # 3초 간격으로 , output area에 내용이 번역완성되었는지 체크,
        # 20번 시도하여 반환값없을시 그냥 break;
        while split_trans == "":
            time.sleep(0.5)
            count = count + 1
            split_trans = self.get_element_attribute(self.output_xpath, 'innerText')
            # 20번 시도했으믄 그냥 break
            if count >= 5:
                break;
        time.sleep(0.5)
        return split_trans

    # 구글 번역 : sk 출발언어, tk 목표언어, st 내용
    def google_trans(self, sk, tk, st):
        text_trans = ""
        url = f'https://translate.google.com/?sl={sk}&tl={tk}'

        # 번역하고자 하는 string의 길이가 3500넘을시

        self.get_url(url)

        ## \n 포함시 줄바꾸기로 짤라서 번역하고 다시 줄바꾸기 붙이기.
        if "\n" in st:
            split_texts = st.split("\n")
            for split_text in split_texts:
                if (len(split_text)):
                    split_trans = self.paste_trans(split_text)
                    print('.', end='')
                    # 번역된 내용을 title_trans에 붙이기.
                    text_trans = text_trans + split_trans + '\n'
        # \n포함 않할시
        else:
            # 긴 내용시 강제로 3500으로 짤라서 번역.
            if (len(st)) > 3500:
                split_texts = self.text_wrap(st, 3500)
                for split_text in split_texts:
                    if (len(split_text)):
                        split_trans = self.paste_trans(split_text)
                        # 번역된 내용을 title_trans에 붙이기.
                        text_trans = text_trans + split_trans + '\n'
            # 한번에 번역 가능시 그냥 번역.
            else:
                text_trans = self.paste_trans(st)
        return text_trans
