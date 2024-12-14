from utils import *
import re
import random

# Initial prompt template for generating C++11 code based on a problem description.
init_prompt = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

# Prompt template to provide feedback when the generated code fails tests.
error_prompt = """Your code failed the following tests:
{error_description}
Give it another try.
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

# Prompt template to request critique and advice when code fails tests.
critic_prompt = """
Your code failed the following tests:
{error_description}
In this step, you DO NOT generate code. Instead, you are required to summarize the error messages and give advice on re-generating.
"""

# Prompt template to request the selection of an algorithm category.
select_ctg_prompt = """
Select an algorithm category for the following competitive programming question: 
{problem_description}
Available Choices:
{algorithms}
You should directly and only output the name of the selected algorithm. NO OTHER WORDS. 
"""

# Prompt template for generating Python code based on an algorithm description.
exploit_alg_prompt = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
You can refer to the algorithm below:
{algorithm_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
"""

# Complete prompt template for generating C++11 code based on a problem description.
complete_prompt = """
Complete an incomplete C++11 solution for the following competitive programming question: 
{problem_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
The incomplete code is as follows. You should not modify the finished part.
```cpp
{incomplete_code}
```
"""

modify_prompt = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
Here is a previous version of your code. Check whether there are mistakes in it and correct them. You can also refract the code to make it better.
```cpp
{previous_code}
```
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""
# Base class for code generation, which contains shared methods and attributes.
class Generator:
    def __init__(self, problem_description):
        self.problem_description = problem_description  # Problem description as input.
        self.history = []  # History of interactions with the generator.

    # Abstract method for generating code; must be implemented in subclasses.
    def generate_code(self, feedback: str=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    # Abstract method for self-criticism; must be implemented in subclasses.
    def self_criticize(self, feedback: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    # Abstract method for selecting an algorithm category; must be implemented in subclasses.
    def select_category(self, choice: List[str]) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    # Abstract method for generating code using a specific algorithm; must be implemented in subclasses.
    def generate_code_w_alg(self, alg: str=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    # Helper method to extract Python code from a response using regex.
    def _extract_python_code(self, response: str) -> str:
        pattern = r'```python(.*?)```'  # Regex pattern to match Python code blocks.
        match = re.findall(pattern, response, re.DOTALL)
        if len(match) > 0:
            code = match[0]
        else:
            code = "# Invalid output formate. No python code generated."
        return code
    
    # Helper method to extract C++11 code from a response using regex.
    def _extract_c_code(self, response: str) -> str:
        pattern = r'```cpp(.*?)```'  # Regex pattern to match C++11 code blocks.
        match = re.findall(pattern, response, re.DOTALL)
        if len(match) > 0:
            code = match[0]
        else:
            code = "# Invalid output formate. No c++11 code generated."
        return code

# Class for generating code using the GPT-4 model.
class GPT4Generator(Generator):
    def __init__(self, problem_description):
        super().__init__(problem_description)  # Initialize the base class.

    # Method to generate code with optional feedback.
    def generate_code(self, feedback: str=None) -> str:
        if feedback:  # Use error feedback if provided.
            prompt = error_prompt.format(error_description=feedback)
        else:  # Otherwise, use the initial problem description prompt.
            prompt = init_prompt.format(problem_description=self.problem_description)
        message = {"role": "user", "content": prompt}
        self.history.append(message)  # Add the prompt to the history.
        response = generate_response(messages=self.history)  # Generate a response.
        self.history.append({"role": "assistant", "content": response})  # Add the response to the history.
        return self._extract_c_code(response)  # Extract C++11 code from the response.
    
    # Method to critique the generated code based on feedback.
    def self_criticize(self, feedback: str) -> str:
        prompt = critic_prompt.format(error_description=feedback)
        message = {"role": "user", "content": prompt}
        self.history.append(message)
        response = generate_response(messages=self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
    
    # Method to select an algorithm category from a list of choices.
    def select_category(self, choices: List[str]) -> str:
        prompt = select_ctg_prompt.format(problem_description=self.problem_description, algorithms = ", ".join(choices))
        message = {"role": "user", "content": prompt}
        response = generate_response(messages=[message])
        if response in choices:
            return response  # Return the response if it matches one of the choices.
        else:
            return random.choice(choices)  # Otherwise, randomly choose a category.
            
    # Method to generate code using a specific algorithm description.
    def generate_code_w_alg(self, alg: str=None) -> str:
        prompt = exploit_alg_prompt.format(problem_description=self.problem_description, algorithm_description = alg)
        message = {"role": "user", "content": prompt}
        response = generate_response(messages=[message])
        return self._extract_c_code(response)

# Class for generating code using the GLM model.
class GLMGenerator(Generator):
    def __init__(self, problem_description):
        super().__init__(problem_description)

    # Similar methods as GPT4Generator, adjusted for GLM model usage.
    def generate_code(self, feedback: str=None) -> str:
        if feedback:
            prompt = error_prompt.format(error_description=feedback)
        else:
            prompt = init_prompt.format(problem_description=self.problem_description)
        message = {"role": "user", "content": prompt}
        self.history.append(message)
        response = generate_response(messages=self.history)
        self.history.append({"role": "assistant", "content": response})
        return self._extract_c_code(response)
    
    def self_criticize(self, feedback: str) -> str:
        prompt = critic_prompt.format(error_description=feedback)
        message = {"role": "user", "content": prompt}
        self.history.append(message)
        response = generate_response(messages=self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
    
    def select_category(self, choices: List[str]) -> str:
        prompt = select_ctg_prompt.format(problem_description=self.problem_description, algorithms = ", ".join(choices))
        message = {"role": "user", "content": prompt}
        response = generate_response(messages=[message])
        if response in choices:
            return response
        else:
            return random.choice(choices)
            
    def generate_code_w_alg(self, alg: str=None) -> str:
        prompt = exploit_alg_prompt.format(problem_description=self.problem_description, algorithm_description = alg)
        message = {"role": "user", "content": prompt}
        response = generate_response(messages=[message])
        return self._extract_c_code(response)
    
    
# Class for generating code using the GLM model.
class GLMGeneratorTree(Generator):
    def __init__(self, problem_description):
        super().__init__(problem_description)

    # Similar methods as GPT4Generator, adjusted for GLM model usage.
    def generate_code(self, n: int = 1, feedback: str = None, policy = "append") -> List[str]:
        if feedback:
            if policy == "append":
                prompt = complete_prompt.format(problem_description=self.problem_description, incomplete_code=feedback)
            elif policy == "modify":
                prompt = modify_prompt.format(problem_description=self.problem_description, previous_code=feedback)
            else :
                raise ValueError("Invalid policy. Must be 'append' or 'modify'.")
        else:
            prompt = init_prompt.format(problem_description=self.problem_description)
        
        message = {"role": "user", "content": prompt}
        rsp_list = generate_response(messages=[message], n=n)
        return [self._extract_c_code(response) for response in rsp_list]

# Dictionary mapping generator types to their respective classes.
GENERATOR_TYPE = {
    "gpt-4o": GPT4Generator,
    "glm": GLMGenerator,
    "glm_tree": GLMGeneratorTree
}