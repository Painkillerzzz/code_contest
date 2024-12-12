import requests
import json
import time
import sys
if len(sys.argv) < 2:
    print("Please provide the competition ID.")
    exit()
BACKEND_URL = "https://mycopai.net9.org:9443"
path_to_json = './results/data.json' # NOTE replace this with your json path

# 读取 JSON 文件
with open(path_to_json) as f:
    data = json.load(f)

USERNAME = "Painkiller"
PASSWORD = "zxy1029384756"

# Client login, get JWT token
response = requests.post(
    BACKEND_URL + "/login", 
    json={"userName": USERNAME, "password": PASSWORD}, 
)
token = response.json()["token"]

# POST to certain competition with {id}, get allocated AI {ai_id}

# 从参数中解析 ID

id = sys.argv[1]

ai_name = "New_AI"
api = "www.fakeapi.com"
response = requests.post(
    BACKEND_URL + f"/competition/{id}/myai", 
    headers={"Authorization": token},
    json={"ai_name": ai_name, "api": api},
)

ai_id = response.json().get("ai_id")


# 检查 AI 是否已分配
if ai_id is None:
    print("Error: AI ID not found in the response.")
    exit()

# 准备文件上传的数据
files = {}
for index, item in enumerate(data):
    # 使用 code_file_{index}.txt 作为上传的文件名
    code_file_name = f"code_file_{index}.txt"
    files[f"codes[{index}][question_id]"] = (None, str(item["question_id"]))  # 只传递 question_id
    files[f"codes[{index}][code_file]"] = (code_file_name, item["code_file"], "text/plain")  # 上传代码文件

# 上传文件
response = requests.post(
    BACKEND_URL + f"/evaluate/{ai_id}",
    headers={"Authorization": token},
    files=files,
)

# 可选：查询状态直到完成
while True:
    response = requests.get(
        BACKEND_URL + f"/competition/{id}/myai/{ai_id}",
        headers={"Authorization": token},
    )
    if response.json()["status"] == "completed":
        print("Completed!")
        print(response.json())
        break
    else:
        print("Waiting for evaluation...")
        time.sleep(5)
