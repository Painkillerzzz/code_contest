import os
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict


def run_single_input(exe_file_path: str, input_data: str, timeout: int) -> Dict[str, str]:
    """
    Run the compiled executable with a single input.

    Args:
        exe_file_path (str): Path to the compiled executable.
        input_data (str): The input to provide to the executable.
        timeout (int): Maximum execution time in seconds.

    Returns:
        Dict[str, str]: A dictionary containing "stdout", "stderr", "error", and "time_elapsed".
    """
    start_time = time.time()
    result = {
        "stdout": "",
        "stderr": "",
        "error": "",
        "time_elapsed": 0
    }
    try:
        process = subprocess.Popen(
            [exe_file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_data, timeout=timeout)
        result["stdout"] = stdout.strip()
        result["stderr"] = stderr.strip()
        process.wait()
        result["error"] = "" if process.returncode == 0 else f"Return code: {process.returncode}"
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        result["error"] = f"Execution timed out after {timeout} seconds"
    except Exception as e:
        result["error"] = str(e)
    finally:
        result["time_elapsed"] = time.time() - start_time
    return result


def run_code_with_inputs(code: str, inputs: List[str], timeout: int = 5) -> List[Dict[str, str]]:
    """
    Compile and run the provided C++11 code with multiple inputs in parallel, capturing output or errors.

    Args:
        code (str): The C++11 code as a string.
        inputs (List[str]): A list of inputs to provide to the executable.
        timeout (int): The maximum execution time in seconds for each input (default: 5 seconds).

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing "stdout", "stderr", "error", and "time_elapsed".
    """
    results = []
    tmp_dir = "tmp"

    # Ensure the tmp directory exists
    os.makedirs(tmp_dir, exist_ok=True)

    try:
        # Create a temporary file for the C++ source code
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", dir=tmp_dir) as cpp_file:
            cpp_file.write(code.encode("utf-8"))
            cpp_file_path = cpp_file.name

        # Create a temporary file path for the compiled executable
        exe_file_path = cpp_file_path.replace(".cpp", ".exe")

        # Compile the C++ code
        compile_cmd = ["g++", "-std=c++11", cpp_file_path, "-o", exe_file_path]
        compile_process = subprocess.run(
            compile_cmd, capture_output=True, text=True
        )

        # Check if compilation was successful
        if compile_process.returncode != 0:
            return [{
                "stdout": "",
                "stderr": compile_process.stderr,
                "error": "Compilation failed",
                "time_elapsed": 0
            }] * len(inputs)

        # Run all inputs in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            future_to_input = {
                executor.submit(run_single_input, exe_file_path, input_data, timeout): input_data
                for input_data in inputs
            }

            for future in as_completed(future_to_input):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({
                        "stdout": "",
                        "stderr": "",
                        "error": str(e),
                        "time_elapsed": 0
                    })

    except Exception as e:
        # Handle unexpected exceptions
        results = [{
            "stdout": "",
            "stderr": "",
            "error": str(e),
            "time_elapsed": 0
        }] * len(inputs)
    finally:
        # Clean up temporary files
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(exe_file_path):
            os.remove(exe_file_path)

    return results


# Example usage
if __name__ == "__main__":
    cpp_code = """
    #include <iostream>
    #include <thread>
    #include <chrono>
    using namespace std;
    int main() {
        int duration;
        cin >> duration;
        this_thread::sleep_for(chrono::seconds(duration));
        cout << "Slept for " << duration << " seconds." << endl;
        return 0;
    }
    """
    inputs = ["3", "5", "2"]  # Each input represents a sleep duration
    start_time = time.time()
    results = run_code_with_inputs(cpp_code, inputs)
    total_elapsed_time = time.time() - start_time

    for i, result in enumerate(results):
        print(f"Input {i + 1}: {inputs[i]}")
        print("STDOUT:", result["stdout"])
        print("STDERR:", result["stderr"])
        print("ERROR:", result["error"])
        print("Time Elapsed:", result["time_elapsed"])
        print("-" * 30)

    print(f"Total Elapsed Time for All Runs: {total_elapsed_time:.2f} seconds")
