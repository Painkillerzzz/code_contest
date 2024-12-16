import os
import sys
import json
import argparse
from openai import OpenAI
from zhipuai import ZhipuAI
from typing import List, Dict, Any

client = ZhipuAI(api_key="98903f4152cd6b8cc8a1d4d16ff11a59.JO98BUYm6Bl4YVFf")

def generate_response(messages: List[Dict[str, str]], n: int = 1) -> str:
    """
    Generate a response from the model using the provided messages.

    Args:
        messages (List[Dict[str, str]]): A list of messages forming the conversation history.

    Returns:
        str: The response content from the model.
    """
    rsp_list = []
    for _ in range(n):
        try:
            # Request a chat completion from the model.
            response = client.chat.completions.create(
                model="codegeex-4",  # Specify the model to use.
                messages=messages,  # Provide the conversation history.
                temperature=1.0,  # Set temperature for deterministic responses.
            ).choices[0].message.content
            rsp_list.append(response)
        except:
            # Return an empty string in case of an error.
            pass

    return rsp_list

def parse_args():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Code Evaluation Tool")
    parser.add_argument('-md', '--model_name', type=str, required=True, help='Name of the model to use')
    parser.add_argument('-mt', '--method_name', type=str, help='Name of the method to execute')
    parser.add_argument('-i', '--iterations', type=int, default=3, help='Number of iterations to perform')
    args = parser.parse_args()
    return args

def read_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """
    Read a JSONL file and parse its contents into a list of dictionaries.

    Args:
        file_path (str): Path to the JSONL file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the file contents.
    """
    data_list: List[Dict[str, Any]] = []  # Initialize an empty list to store data.
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the file line by line.
        for line in file:
            data: Dict[str, Any] = json.loads(line)  # Parse each line as JSON.
            data_list.append(data)  # Append the parsed dictionary to the list.
    return data_list
