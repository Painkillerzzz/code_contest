import json

method_list = ["mcts"]
results = {}
log = {}

for method in method_list:
    result_path = f"./results/data_{method}_old.json"
    log_path = f"./results/log_{method}_old.json"
    with open(result_path, "r") as f:
        results[method] = json.load(f)
    with open(log_path, "r") as f:
        log[method] = json.load(f)
        
    for case in log[method]:
        if case["revision"] < 0:
            case["revision"] += 1 
        assert case["revision"] >= 0
        
    
    with open(log_path, "w") as f:
        json.dump(log[method], f, indent=4)
        
# for method, result in log.items():
#     score_list = [case["score"] for case in result]
#     score = sum(score_list) / len(score_list)
#     print(method, score)