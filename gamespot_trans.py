import json, time, os, glob, logging, requests
from dotenv import load_dotenv
import _webbrowser_helper

load_dotenv()
logging.basicConfig(filename='./logs/gamespot_trans.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

## init values
driver_path = os.getenv('DRIVER_PATH')
api_server = os.getenv('API_SERVER')

## browser
browser = _webbrowser_helper.MyBrowserHelper(f'https://translate.google.com/', driver_path)

## json 파일 읽기
json_dir = os.getenv('JSON_DIR')

# 지정폴더밑에,json파일들의 목록 읽어오기
json_files = glob.glob(os.path.join(json_dir, '*.json'))
# 루프로 매개의 파일이름 읽어오기
for json_file in json_files:
    # 파일을 json 형식으로 읽기
    with open(json_file) as file:
        try:
            page_dict = json.load(file)
            if page_dict:
                ##############################################################################################
                ## 번역 부분 google_trans(sk,tk,st) sk: from_lang , kt: to_lang , st : text_ori
                print('')
                print('##############################################################################################')
                print(f'## {json_file} .')
                if (os.getenv('IS_KO') == '1'):
                    print('#text_ko', end='')
                    page_dict['page_text_ko'] = browser.google_trans('en', 'ko', page_dict['page_text_en'])
                    page_dict['page_title_ko'] = browser.google_trans('en', 'ko', page_dict['page_title_en'])
                    page_dict['page_description_ko'] = browser.google_trans('en', 'ko', page_dict['page_description_en'])

                if (os.getenv('IS_CN') == '1'):
                    print('#text_cn', end='')
                    page_dict['page_text_cn'] = browser.google_trans('en', 'zh-CN', page_dict['page_text_en'])
                    page_dict['page_title_cn'] = browser.google_trans('en', 'zh-CN', page_dict['page_title_en'])
                    page_dict['page_description_cn'] = browser.google_trans('en', 'zh-CN', page_dict['page_description_en'])
                ##############################################################################################
                ## 파일 재저장.
                with open(f'./datas/{page_dict["page_title_en"]}.json', 'w', encoding='utf-8') as outfile:
                    json.dump(page_dict, outfile)
                    print('  #refresh jsonFile ok.')

                ##############################################################################################
                ## db 갱신.
                time.sleep(1)
                res = requests.post(f'{api_server}/api/posts', json=page_dict)
                # 상태코드 200일시 해당 파일 삭제
                if (res.status_code == 200):
                    os.remove(json_file)
                    print(f'ok : {json_file}')
                else:
                    print(f'error :{page_dict} , : code : {res.status_code}')
                print('##############################################################################################')
        except Exception as e:
            logging.error(e)
