import subprocess
import json
from tqdm import tqdm
from typing import Any, Dict, List, Tuple
from generator import Generator, GENERATOR_TYPE
from utils import read_jsonl, parse_args

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
    # method_name = args.method_name
    # iterations = args.iterations

    data = read_jsonl("./data/data.jsonl")
    
    results = []
    
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
        code_file = solve_problem(test_case["description"], None, test_case["inputs"], test_case["outputs"])
        results.append({
            "question_id": test_case["id"],
            "code_file": code_file,
        })
        
    with open("./results/data.json", "w") as f:
        json.dump(results, f, indent=4)
