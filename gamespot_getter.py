## gamespot.com 에 뉴스 끌어오기.
import json, time, os, logging, re
import _webbrowser_helper, _init
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='./logs/gamespot_getter.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# init values
domain = os.getenv('DOMAIN')
driver_path = os.getenv('DRIVER_PATH')
browser = _webbrowser_helper.MyBrowserHelper(f'https://bing.com', driver_path)
start_page = int(os.getenv('START_PAGE'))
comm = _init.CommonFucntion()
print('')
while start_page > 0:
    browser.get_url(f'{domain}/news/?page={start_page}')
    _urls = []
    page_dicts = []

    ######################################################################################################
    ## page 1 top 6 articles
    if start_page == 1:
        _elements = browser.get_elements('//section[@class="promo--container container row span12"]/a')
        for _element in _elements:
            _urls.append(_element.get_attribute('href'))
        _elements = browser.get_elements('//div[@class="promo-strip__item  "]/a')
        for _element in _elements:
            _urls.append(_element.get_attribute('href'))

    ######################################################################################################
    ## normal articles
    _elements = browser.get_elements('//a[@class="card-item__link text-decoration--none "]')
    for _element in _elements:
        _urls.append(_element.get_attribute('href'))

    print('###########################################################################')
    print(f'page: {start_page} --> items: {len(_urls)}')
    i = 0
    for _url in _urls:
        i = i + 1
        try:
            ################################################################################################
            # ./datas/[url].json is there ==> out
            _pid = comm.get_pid(_url)
            if comm.json_exists('./datas/' + _pid + '.json'):
                continue
            browser.get_url(_url)
            page_dict = {}
            if browser.is_there("Feature Article"):
                page_dict = {
                    "page_url": _url,
                    "page_pid": _pid,
                    "page_title_en": comm.remove_emojis(
                        comm.remove_spe_char(browser.get_element_text('//*[@class="kubrick-info__title"]'))),
                    "page_title_ko": "",
                    "page_title_cn": "",
                    "page_description_en": comm.remove_emojis(browser.get_element_text('//*[@class="news-deck"]')),
                    "page_description_ko": "",
                    "page_description_cn": "",
                    "page_author": browser.get_element_text('//*[@class="byline-author__name"]'),
                    "page_date": browser.get_element_attribute('//*[@class="news-byline"]/time', 'datetime'),
                    "page_text_html": browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerHTML'),
                    "page_text_en": comm.remove_emojis(browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerText')),
                    "page_text_ko": '',
                    "page_text_cn": '',
                    "page_tags": browser.get_elements_text('//a[@class="font-base"]'),
                    "page_images": browser.get_elements_src_by_css_selector('article > section img'),
                    "page_videos": ''
                }
            else:
                page_dict = {
                    "page_url": _url,
                    "page_pid": _pid,
                    "page_title_en": comm.remove_emojis(
                        comm.remove_spe_char(browser.get_element_text('//*[@class="news-title instapaper_title entry-title type-headline"]'))),
                    "page_title_ko": "",
                    "page_title_cn": "",
                    "page_description_en": comm.remove_emojis(browser.get_element_text('//*[@class="news-deck type-subheader"]')),
                    "page_description_ko": "",
                    "page_description_cn": "",
                    "page_author": browser.get_element_text('//*[@class="byline-author__name"]'),
                    "page_date": browser.get_element_attribute('//*[@class="news-byline pull-left text-base no-rhythm"]/time', 'datetime'),
                    "page_text_html": browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerHTML'),
                    "page_text_en": comm.remove_emojis(browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]', 'innerText')),
                    "page_text_ko": '',
                    "page_text_cn": '',
                    "page_tags": browser.get_elements_text('//a[@class="font-base"]'),
                    "page_images": browser.get_elements_src_by_css_selector('article > section img'),
                    "page_videos": ''
                }
            # page_dict['page_text_ko'] = trans(browser, 'ko', page_dict['page_text_en'])
            # page_dict['page_text_cn'] = trans(browser, 'cn', page_dict['page_text_en'])
            # page_dict['page_title_ko'] = trans(browser, 'ko', page_dict['page_title_en'])
            # page_dict['page_title_cn'] = trans(browser, 'cn', page_dict['page_title_en'])
            # page_dict['page_description_ko'] = trans(browser, 'ko', page_dict['page_description_en'])
            # page_dict['page_description_cn'] = trans(browser, 'cn', page_dict['page_description_en'])
            page_dicts.append(page_dict)
            # json 파일로 저장. api post를 위한 중간 save 작업.
            with open(f'./datas/{_pid}.json', 'w', encoding='utf-8') as outfile:
                json.dump(page_dict, outfile)
            print(f'{str(i)} / {len(_urls)} : {page_dict["page_title_en"]}')
        except Exception as e:
            logging.error(e)

    print('###########################################################################')
    # print(page_dicts)
    start_page = start_page - 1
print('OK!')
