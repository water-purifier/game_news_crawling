## gamespot.com 에 뉴스 끌어오기.
import json, time, os, glob, logging, requests
import _webbrowser_helper, _init
from dotenv import load_dotenv


def job():
    ################################################################################################################################
    # init values
    load_dotenv()
    logging.basicConfig(filename='./logs/service_start.log', level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    domain = os.getenv('DOMAIN')
    driver_path = os.getenv('DRIVER_PATH')
    start_page = int(os.getenv('START_PAGE'))
    api_server = os.getenv('API_SERVER')
    comm = _init.CommonFucntion()
    browser = _webbrowser_helper.MyBrowserHelper(f'https://bing.com', driver_path)
    print('init value OK . service starting!')
    # init end
    ################################################################################################################################

    ################################################################################################################################
    # getter start  =======  page_dict 가져오기 ==> datas에 저장.
    while start_page > 0:
        browser.get_url(f'{domain}/news/?page={start_page}')
        _urls = []
        page_dicts = []

        ######################################################################################################
        ## page 1 top 6 articles
        if start_page == 1:
            _elements = browser.get_elements('//section[@class="promo--container container row span12"]/a')
            for _element in _elements:
                try:
                    _urls.append(_element.get_attribute('href'))
                except Exception as e:
                    logging.error(e)
            _elements = browser.get_elements('//div[@class="promo-strip__item "]/a')
            for _element in _elements:
                try:
                    _urls.append(_element.get_attribute('href'))
                except Exception as e:
                    logging.error(e)
        ######################################################################################################
        ## normal articles
        _elements = browser.get_elements('//a[@class="card-item__link text-decoration--none "]')
        for _element in _elements:
            try:
                _urls.append(_element.get_attribute('href'))
            except Exception as e:
                logging.error(e)

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
                        "page_text_html": browser.get_element_attribute(
                            '//*[@class="js-content-entity-body content-entity-body"]', 'innerHTML'),
                        "page_text_en": comm.remove_emojis(
                            browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]',
                                                          'innerText')),
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
                            comm.remove_spe_char(browser.get_element_text(
                                '//*[@class="news-title instapaper_title entry-title type-headline"]'))),
                        "page_title_ko": "",
                        "page_title_cn": "",
                        "page_description_en": comm.remove_emojis(
                            browser.get_element_text('//*[@class="news-deck type-subheader"]')),
                        "page_description_ko": "",
                        "page_description_cn": "",
                        "page_author": browser.get_element_text('//*[@class="byline-author__name"]'),
                        "page_date": browser.get_element_attribute(
                            '//*[@class="news-byline pull-left text-base no-rhythm"]/time', 'datetime'),
                        "page_text_html": browser.get_element_attribute(
                            '//*[@class="js-content-entity-body content-entity-body"]', 'innerHTML'),
                        "page_text_en": comm.remove_emojis(
                            browser.get_element_attribute('//*[@class="js-content-entity-body content-entity-body"]',
                                                          'innerText')),
                        "page_text_ko": '',
                        "page_text_cn": '',
                        "page_tags": browser.get_elements_text('//a[@class="font-base"]'),
                        "page_images": browser.get_elements_src_by_css_selector('article > section img'),
                        "page_videos": ''
                    }

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
    print('getter end!')
    # getter end
    ################################################################################################################################

    ################################################################################################################################
    # setter start ======= datas에 json 을 번역 , api_server에 post
    # json 파일 읽기
    json_dir = os.getenv('JSON_DIR')

    # 지정폴더밑에,json파일들의 목록 읽어오기
    json_files = glob.glob(os.path.join(json_dir, '*.json'))
    # 루프로 매개의 파일이름 읽어오기
    for json_file in json_files:
        # 파일을 json 형식으로 읽기
        with open(json_file) as file:
            page_dict = json.load(file)
            if page_dict:
                # datas_ok/1100-1343422.json 있을시 번역 패스, 추가 패스.
                if comm.json_exists('./datas_ok/' + page_dict['page_pid'] + '.json'):
                    continue
                ##############################################################################################
                #  번역 부분 google_trans(sk,tk,st) sk: from_lang , kt: to_lang , st : text_ori
                print('')
                print('##############################################################################################')
                print(f'## {json_file} .')
                try:
                    if os.getenv('IS_KO') == '1':
                        print('#text_ko', end='')
                        page_dict['page_text_ko'] = browser.google_trans('en', 'ko', page_dict['page_text_en'])
                        page_dict['page_title_ko'] = browser.google_trans('en', 'ko', page_dict['page_title_en'])
                        page_dict['page_description_ko'] = browser.google_trans('en', 'ko',
                                                                                page_dict['page_description_en'])

                    if os.getenv('IS_CN') == '1':
                        print('#text_cn', end='')
                        page_dict['page_text_cn'] = browser.google_trans('en', 'zh-CN', page_dict['page_text_en'])
                        page_dict['page_title_cn'] = browser.google_trans('en', 'zh-CN', page_dict['page_title_en'])
                        page_dict['page_description_cn'] = browser.google_trans('en', 'zh-CN',
                                                                                page_dict['page_description_en'])
                except Exception as e:
                    logging.error(e)

                ##############################################################################################
                #  db 갱신.
                time.sleep(0.5)
                try:
                    res = requests.post(f'{api_server}/api/posts', json=page_dict)
                    # 상태코드 200일시 해당 파일 삭제
                    if res.status_code == 200:
                        print(f'ok : {json_file}')
                    elif res.status_code == 202:
                        print(f'exists : {json_file}')
                    else:
                        logging.error(f'error :{page_dict} , : code : {res.status_code}')
                except Exception as e:
                    logging.error(e)

                ##############################################################################################
                #  파일 재저장.
                try:
                    with open(f'./datas_ok/{page_dict["page_pid"]}.json', 'w', encoding='utf-8') as outfile:
                        json.dump(page_dict, outfile)
                        print('  #refresh jsonFile ok.')
                except Exception as e:
                    logging.error(e)

                print('##############################################################################################')
    print('setter end!')
    # setter end
    ################################################################################################################################

    ################################################################################################################################
    # next_js : npm run build ; pm2 restart 0 ==> 나 미쳤다, 너무 잘한다. 문제해결능력 갑~~!!!
    print('next web server rebuilding && restarting')
    command_line = "ssh funcode@iqiafan.com -p 20022 'cd ~/iqiafan.v2/game_news_next_js/; source ~/.nvm/nvm.sh ;npm run build; pm2 restart 0'"
    os.system(command_line)
    print(f'all service is done. loading 3 hours')


# first just run once!

# schedule.every().day.at("06:18").do(job)
# schedule.every(3).hours.do(job)
# schedule.every(10).seconds.do(job)

while True:
    job()
    time.sleep(18000)
