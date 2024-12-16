from utils import *
import re
import random

# Initial prompt template for generating C++11 code based on a problem description.
init_prompt_en = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

init_prompt = """
以下是一个编程竞赛问题：
{problem_description}
请你提供一个 C++11 的答案。你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
请你使用标准C++11，不要使用不在标准库中的第三方库。
"""


# Prompt template to provide feedback when the generated code fails tests.
error_prompt_en = """Your code failed the following tests:
{error_description}
Give it another try.
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

error_prompt = """你的代码在以下测例中出现错误：
{error_description}
请你重新提供答案，再试一次。
你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
请你使用标准C++11，不要使用不在标准库中的第三方库。
"""


# Prompt template to request critique and advice when code fails tests.
critic_prompt_en = """
Your code failed the following tests:
{error_description}
In this step, you DO NOT generate code. Instead, you are required to summarize the error messages and give advice on re-generating.
"""

critic_prompt = """
你的代码在以下测例中出现错误：
{error_description}
在这一步中，你不需要生成代码。相反，你需要总结错误信息并给出重新生成代码的建议。
"""

# Prompt template to request the selection of an algorithm category.
select_ctg_prompt_en = """
Select an algorithm category for the following competitive programming question: 
{problem_description}
Available Choices:
{algorithms}
You should directly and only output the name of the selected algorithm. NO OTHER WORDS. 
"""

select_ctg_prompt = """
选择一个算法类别，用于解决以下编程竞赛问题：
{problem_description}
以下是可用的选择：
{algorithms}
你应该直接且只输出所选算法的名称。不要输出其他内容。
"""


# Prompt template for generating Python code based on an algorithm description.
exploit_alg_prompt_en = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
You can refer to the algorithm below:
{algorithm_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
"""

exploit_alg_prompt = """
提供一个 C++11 的答案，用于解决以下编程竞赛问题：
{problem_description}
你可以参考以下算法：
{algorithm_description}
你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
"""

# Complete prompt template for generating C++11 code based on a problem description.
complete_prompt_en = """
Complete an incomplete C++11 solution for the following competitive programming question: 
{problem_description}
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
The incomplete code is as follows. You should not modify the finished part.
```cpp
{incomplete_code}
```
"""

complete_prompt = """
提供一个 C++11 的答案，用于解决以下编程竞赛问题：
{problem_description}
你需要完成下面的不完整代码。你不应该修改已完成的部分。
```cpp
{incomplete_code}
```
你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
请你使用标准C++11，不要使用不在标准库中的第三方库。
"""

modify_prompt_en = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
Here is a previous version of your code. Check if there are mistakes in it and correct them. You can also refract the code to make it better.
```cpp
{previous_code}
```
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

modify_prompt = """
提供一个 C++11 的答案，用于解决以下编程竞赛问题：
{problem_description}
这是你之前的代码版本。检查是否有错误并加以纠正。你也可以重构代码以使其更好。
```cpp
{previous_code}
```
你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
请你使用标准C++11，不要使用不在标准库中的第三方库。
"""

cot_init_prompt_en = """
Here is a competitive programming question:
{problem_description}
Analyze the problem and provide your thoughts on the data structures and algorithms that could be used to solve it.
Remember: Your answer should be concise and to the point. Do not provide any code.
"""

cot_init_prompt = """
以下是一个编程竞赛问题：
{problem_description}
请分析问题并提供你对解决问题可能使用的数据结构和算法的看法。
注意：你的回答应该简洁明了，不要提供任何代码。
"""

cot_append_prompt_en = """
Here is a competitive programming question:
{problem_description}
Your teammates has already provided the following thoughts on the problem:
{previous_thoughts}
Please provide your thoughts on the problem.
Remember: Your answer should be concise and to the point. Do not provide any code.
"""

cot_append_prompt = """
以下是一个编程竞赛问题：
{problem_description}
你的队友已经提供了以下关于问题的想法：
{previous_thoughts}
请提供你对问题的看法。
注意：你的回答应该简洁明了，不要提供任何代码。
"""


cot_generate_prompt_en = """
Provide a C++11 solution for the following competitive programming question: 
{problem_description}
Your teammates has already provided the following thoughts on the problem:
{previous_thoughts}
Please generate a C++11 solution for the problem.
Your code should be enclosed in triple backticks like so: ```cpp YOUR CODE HERE```. Use the backticks for your code only.
The standard is C++11, please do not use third-party libraries that are not included in the standard library.
"""

cot_generate_prompt = """
提供一个 C++11 的答案，用于解决以下编程竞赛问题：
{problem_description}
你的队友已经提供了以下关于问题的想法：
{previous_thoughts}
请提供一个 C++11 的解决方案。
你的代码应该被三个反引号包围，像这样：```cpp YOUR CODE HERE```，且只用反引号包围你的代码。
请你使用标准C++11，不要使用不在标准库中的第三方库。
"""


# Base class for code generation, which contains shared methods and attributes.
class Generator:
    def __init__(self, problem_description):
        self.problem_description = problem_description  # Problem description as input.
        self.history = []  # History of interactions with the generator.

    # Abstract method for generating code; must be implemented in subclasses.
    def generate_code(self, feedback: str=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    # Abstract method for generating thoughts; must be implemented in subclasses.
    def generate_thoughts(self, feedback: str=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
    # Abstract method for generating code with previous thoughts; must be implemented in subclasses.
    def generate_code_w_thoughts(self, feedback: str=None) -> str:
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
    def generate_thoughts(self, n : int = 1, feedback: list[str] = [], policy = "append") -> List[str]:
        if feedback and len(feedback) > 0:
            prompt = cot_append_prompt.format(problem_description=self.problem_description,previous_thoughts="\n\n".join(feedback) )
        else:
            prompt = cot_init_prompt.format(problem_description=self.problem_description)
        message = {"role": "user", "content": prompt}
        rsp_list = generate_response(messages=[message], n=n)
        return rsp_list
    def generate_code_w_thoughts(self, thought:str = "", thoughts: list[str] = []):
        if thoughts == None or len(thoughts) == 0:
            thoughts = [thought]
        else:
            thoughts.append(thought)
        prompt = cot_generate_prompt.format(problem_description=self.problem_description, previous_thoughts="\n\n".join(thoughts))
        message = {"role": "user", "content": prompt}
        print(prompt)
        response = generate_response(messages=[message])[0]
        return self._extract_c_code(response), thoughts
# Dictionary mapping generator types to their respective classes.
GENERATOR_TYPE = {
    "gpt-4o": GPT4Generator,
    "glm": GLMGenerator,
    "glm_tree": GLMGeneratorTree
}