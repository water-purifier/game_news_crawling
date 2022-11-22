import json, time, os, glob, logging, requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='./logs/gamespot_setter.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

## init values
api_server = os.getenv('API_SERVER')
## json 파일 읽기

json_datas = []
json_dir = os.getenv('JSON_DIR')

# 지정폴더밑에,json파일들의 목록 읽어오기
json_files = glob.glob(os.path.join(json_dir, '*.json'))
# 루프로 매개의 파일이름 읽어오기
for json_file in json_files:
    # 파일을 json 형식으로 읽기
    with open(json_file) as file:
        json_data = json.load(file)
        try:
            if json_data:
                time.sleep(0.5)
                res = requests.post(f'{api_server}/api/posts', json=json_data)
                # 상태코드 200일시 해당 파일 삭제
                if (res.status_code == 200):
                    # os.remove(json_file)
                    print(res.text)
                else:
                    print(f'error : code : {res.status_code}')
        except Exception as e:
            logging.error(e)
