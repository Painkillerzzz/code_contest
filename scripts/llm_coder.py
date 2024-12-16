import json, os
from tqdm import tqdm
from typing import Any, List
from mcts import MCTSTree
from treeofthoughts import TreeofToughts
from evaluator import Evaluator
from generator import Generator, GENERATOR_TYPE
from utils import read_jsonl, parse_args
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def check_output(expected_output: Any, actual_output: Any) -> bool:
    return expected_output.strip() == actual_output.strip()

# def evaluate_problem(problem_description: str, method: str, public_tests: Dict[str, List[str]], private_tests: Dict[str, List[str]],
#                      time_limit: float, memory_limit: int, iterations: int) -> Dict:
#     try:
#         generator: Generator = GENERATOR_TYPE[model_name](problem_description)
#     except KeyError:
#         raise ValueError(f"Model unavailable! Choose from: {list(GENERATOR_TYPE.keys())}")
    
#     evaluation = {
#         "generation": {},
#         "code": [],
#         "public": [],
#         "private": "",
#         "result": ""
#     }
#     code = generator.generate_code()

#     for attempt in range(iterations):
#         # Initialize flag to track if all public tests passed
#         all_public_passed = True
#         error_messages = []
#         log = []
        
#         evaluation["code"].append(code)

#         # Iterate over all public test cases
#         for idx in range(len(public_tests['input'])):
#             test_input = public_tests['input'][idx]
#             expected_output = public_tests['output'][idx]

#             # Run the code
#             status, result = run_code_with_input(code, test_input, time_limit, memory_limit)

#             if status == "Timeout":
#                 all_public_passed = False
#                 error_messages.append(f"- input: `{test_input}` failed: Execution took too long.\n")
#                 log.append(f"Test Case {idx + 1}: Timeout")
#             elif status == "Out of Memory":
#                 all_public_passed = False
#                 error_messages.append(f"- input: `{test_input}` failed: Out of memory.\n")
#                 log.append(f"Test Case {idx + 1}: Out of memory")
#             elif status == "Error":
#                 all_public_passed = False
#                 error_messages.append(f"- input: `{test_input}` failed: \n{result}")
#                 log.append(f"Test Case {idx + 1}: Runtime Error - {result}")
#             else:
#                 if check_output(expected_output, result):
#                     log.append(f"Test Case {idx + 1}: Correct Answer")
#                 else:
#                     all_public_passed = False
#                     error_messages.append(f"- input: `{test_input}` failed: \nExpected output `{expected_output}` but got `{result}`.")
#                     log.append(f"Test Case {idx + 1}: Wrong Answer - Expected {expected_output}, but got {result.strip()}")

#         evaluation["public"].append("; ".join(log))
#         if all_public_passed:
#             break  # Exit the loop if all public tests passed
#         else:
#             if attempt < iterations - 1:
#                 # Regenerate code with feedback
#                 feedback = "\n".join(error_messages)
#                 if method == "self-critic":
#                     generator.self_criticize(feedback=feedback)
#                 code = generator.generate_code(feedback=feedback)
                
#     evaluation["generation"] = generator.history

#     # After public tests, proceed to private tests if public tests passed
#     log = []
#     private_num = len(private_tests['input'])
#     private_passed_cnt = 0

#     for idx in range(private_num):
#         test_input = private_tests['input'][idx]
#         expected_output = private_tests['output'][idx]

#         # Run the code
#         status, result = run_code_with_input(code, test_input, time_limit, memory_limit)

#         if status == "Timeout":
#             log.append(f"Test Case {idx + 1}: Timeout")
#         elif status == "Out of Memory":
#             log.append(f"Test Case {idx + 1}: Out of memory")
#         elif status == "Error":
#             log.append(f"Test Case {idx + 1}: Runtime Error - {result}")
#         else:
#             # Check the result
#             if check_output(expected_output, result):
#                 private_passed_cnt += 1
#                 log.append(f"Test Case {idx + 1}: Correct Answer")
#             else:
#                 log.append(f"Test Case {idx + 1}: Wrong Answer - Expected {expected_output}, but got {result.strip()}")

#     evaluation["private"] = "; ".join(log)
#     evaluation["result"] = "{:.2f}".format(private_passed_cnt / private_num)
        
#     return evaluation

def solve_problem(problem_description: str, method: str = None, inputs: List[str] = None, outputs: List[str] = None) -> str:
    try:
        generator: Generator = GENERATOR_TYPE[model_name](problem_description)
    except KeyError:
        raise ValueError(f"Model unavailable! Choose from: {list(GENERATOR_TYPE.keys())}")
    
    code = generator.generate_code()

    return code

if __name__ == "__main__":
    args = parse_args()
    model_name = args.model_name
    method_name = args.method_name
    # iterations = args.iterations
    
    if method_name in ["mcts", "vanilla","tot"]:
        method_config = config["method"][method_name]
    else:
        raise ValueError(f"Method {method_name} not supported, choose from: mcts, vanilla")
    
    config_str = "_".join([method_name] + [f"{key[0]}_{value}" for key, value in method_config.items()])
    result_path = os.path.join("./results", config_str)
    os.makedirs(result_path, exist_ok=True)
    code_path = os.path.join(result_path, f"code_{config_str}.json")
    log_path = os.path.join(result_path, f"log_{config_str}.json")
    if os.path.isfile(code_path) and os.path.isfile(log_path):
        with open(code_path, "r") as f:
            results = json.load(f)
        with open(log_path, "r") as f:
            log = json.load(f)
    else:
        results = []
        log = []
        
    data = read_jsonl("./data/data.jsonl")
    
    for test_case in tqdm(data, desc="Generating"):
        # result = evaluate_problem(
        #     problem_description=test_case["description"],
        #     method=method_name,
        #     public_tests=test_case["public_tests"],  # Directly pass the entire public_tests list
        #     private_tests=private_tests,  # Assuming private_tests is available
        #     time_limit=time_limit,
        #     memory_limit=test_case["memory_limit_bytes"],  # Assuming memory limit is in bytes
        #     iterations=iterations
        # )
        
        # code_file = solve_problem(test_case["description"], None, test_case["inputs"], test_case["outputs"])
        try:
            generator: Generator = GENERATOR_TYPE[model_name](test_case["description"])
        except KeyError:
            raise ValueError(f"Model unavailable! Choose from: {list(GENERATOR_TYPE.keys())}")
        
        evaluator = Evaluator(test_case["inputs"], test_case["outputs"])
        
        if method_name == "mcts":
            mcts = MCTSTree(generator.generate_code, evaluator.evaluate_code, max_w = method_config["max_w"], step = method_config["step"], budget = method_config["budget"], bp_policy=method_config["bp_policy"],derive_policy=method_config["derive_policy"])
            code_file, score, revision, budget = mcts.search()
        elif method_name == "vanilla":
            best_score = 0
            code_file = ""
            for b in tqdm(range(method_config["budget"]), desc="Vanilla"):
                code = generator.generate_code()[0]
                score = evaluator.evaluate_code(code)
                budget = b + 1
                if score >= best_score:
                    best_score = score
                    code_file = code
                if score == 1.0:
                    code_file = code
                    break
            revision = 0
            score = best_score
        elif method_name == "tot":
            tot = TreeofToughts(generator.generate_thoughts,evaluator.evaluate_code,generator.generate_code_w_thoughts, max_w = method_config["max_w"], step = method_config["step"], budget = method_config["budget"], bp_policy=method_config["bp_policy"], derive_policy=method_config["derive_policy"])
            code_file, score, revision, budget = tot.search()
            print(code_file)
        else:
            raise ValueError(f"Method {method_name} not supported, choose from: mcts, vanilla")
        
        results.append({
            "question_id": test_case["id"],
            "code_file": code_file,
        })
        log.append({
            "question_id": test_case["id"],
            "score": score,
            "revision": revision,
            "budget": budget
        })
        print(f"Test Case {test_case['id']}: {score} {revision} {budget}")
        
        with open(code_path, "w") as f:
            json.dump(results, f, indent=4)
        with open(log_path, "w") as f:
            json.dump(log, f, indent=4)
