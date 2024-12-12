from typing import List
from run_code import run_code_with_inputs

class Evaluator:
    def __init__(self, inputs: List[str], outputs: List[str]):
        self.test_num = len(inputs)
        self.inputs = inputs
        self.outputs = outputs
        
    def evaluate_code(self, code: str) -> float:

        """
        Evaluate the provided C++11 code with multiple inputs and expected outputs.

        Args:
            code (str): The C++11 code as a string.
            inputs (List[str]): A list of inputs to provide to the executable.
            outputs (List[str]): A list of expected outputs corresponding to the inputs.

        Returns:
            float: The accuracy of the code as a float between 0 and 1.
        """
        results = run_code_with_inputs(code, self.inputs)
        score = 0
        for (output, answer) in zip(results, self.outputs):
            if output["stdout"].strip() == answer.strip():
                score += 1
        return score / self.test_num