import json
import os

# 替换为存放子文件夹的根目录路径
base_path = "results"

results = {}
log = {}

# 遍历 base_path 中的所有子文件夹
for subdir in os.listdir(base_path):
    subdir_path = os.path.join(base_path, subdir)

    # 确保处理的是子文件夹
    if os.path.isdir(subdir_path):
        # 构造文件路径
        result_path = os.path.join(subdir_path, f"code_{subdir}.json")
        log_path = os.path.join(subdir_path, f"log_{subdir}.json")

        # 检查文件是否存在并读取内容
        if os.path.exists(result_path):
            with open(result_path, "r") as f:
                results[subdir] = json.load(f)

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                log[subdir] = json.load(f)

# 计算并打印每种方法的平均分数
for method, result in log.items():
    score_list = [case["score"] for case in result if "score" in case]
    if score_list:
        score = sum(score_list) / len(score_list)
        print(f"Method: {method}, Average Score: {score:.2f}")
    else:
        print(f"Method: {method}, No scores available.")
