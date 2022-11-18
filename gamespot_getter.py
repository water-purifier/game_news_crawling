## gamespot.com 에 뉴스 끌어오기.
import json, time, os, logging
import _webbrowser_helper
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='./logs/gamespot_getter.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# init values
domain = os.getenv('DOMAIN')
driver_path = os.getenv('DRIVER_PATH')
browser = _webbrowser_helper.MyBrowserHelper(f'https://google.com', driver_path)
start_page = int(os.getenv('START_PAGE'))


def trans(driver, lang, text):
    sk = "en"
    st = text
    if lang == "ko":
        tk = "ko"
        return browser.google_trans(sk, tk, st)
    elif lang == "cn":
        tk = "zh-CN"
        return browser.google_trans(sk, tk, st)


while start_page > 0:

    browser.get_url(f'{domain}/news/?page={start_page}')
    ## selector
    _elements = browser.get_elements('//a[@class="card-item__link text-decoration--none "]')
    _urls = []
    page_dicts = []
    for _element in _elements:
        _urls.append(_element.get_attribute('href'))
    print(f'page: {start_page} --> items: {len(_urls)}')
    ## 디버깅용으로 urls에서 1개만 컷.
    ## list url
    for _url in _urls:
        try:
            browser.get_url(_url)
            page_dict = {
                "page_url": _url,
                "page_title_en": browser.get_element_text('//*[@class="news-title instapaper_title entry-title type-headline"]'),
                "page_title_ko": "",
                "page_title_cn": "",
                "page_description_en": browser.get_element_text('//*[@class="news-deck type-subheader"]'),
                "page_description_ko": "",
                "page_description_cn": "",
                "page_author": browser.get_element_text('//*[@class="byline-author__name"]'),
                "page_date": browser.get_element_attribute('//*[@class="news-byline pull-left text-base no-rhythm"]/time', 'datetime'),
                "page_text_html": browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerHTML'),
                "page_text_en": browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerText'),
                "page_text_ko": '',
                "page_text_cn": '',
                "page_tags": browser.get_elements_text('//a[@class="font-base"]'),
                "page_images": browser.get_elements_src_by_css_selector('article > section img'),
                "page_videos": ''
            }
            page_dict['page_text_ko'] = trans(browser, 'ko', page_dict['page_text_en'])
            page_dict['page_text_cn'] = trans(browser, 'cn', page_dict['page_text_en'])

            page_dict['page_title_ko'] = trans(browser, 'ko', page_dict['page_title_en'])
            page_dict['page_title_cn'] = trans(browser, 'cn', page_dict['page_title_en'])

            page_dict['page_description_ko'] = trans(browser, 'ko', page_dict['page_description_en'])
            page_dict['page_description_cn'] = trans(browser, 'cn', page_dict['page_description_en'])
            page_dicts.append(page_dict)
            # json 파일로 저장. api post를 위한 중간 save 작업.
            with open(f'./datas/{page_dict["page_title_en"]}_{time.time()}.json', 'w', encoding='utf-8') as outfile:
                json.dump(page_dict, outfile)
            print(page_dict)
        except Exception as e:
            logging.error(e)

    print('\r\n')
    print('########################################')
    print(page_dicts)
    start_page = start_page - 1
print('OK!')
