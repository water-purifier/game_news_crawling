import json, time, os, glob, logging, requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='./logs/gamespot_setter.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(message)s')

## init values
api_server = os.getenv('API_SERVER')
## json 파일 읽기

json_datas = []
json_dir_name = './datas'

# 지정폴더밑에,json파일들의 목록 읽어오기
json_files = glob.glob(os.path.join(json_dir_name, '*.json'))
# 루프로 매개의 파일이름 읽어오기
for json_file in json_files:
    # 파일을 json 형식으로 읽기
    with open(json_file) as file:
        json_data = json.load(file)
        if json_data:
            res = requests.post(f'{api_server}/api/posts', json=json_data)
            # 상태코드 200일시 해당 파일 삭제
            if (res.status_code == 200):
                # os.remove(json_file)
                print('data set ok!')
            else:
                print(f'error : code : {res.status_code}')
## api에 뿌리기
# 루프로 개개의 json 방문.
# for json_data in json_datas:
#     # python - requests - post 로 json을 던지기.
#     res = requests.post(f'{api_server}/api/posts',json=json_data)
#
