import os
import sys
import json
import argparse
from openai import OpenAI
from typing import List, Dict, Any

# Initialize the OpenAI client with API key, base URL, and retry settings.
client = OpenAI(
    api_key="98903f4152cd6b8cc8a1d4d16ff11a59.JO98BUYm6Bl4YVFf",  # Your API key here.
    base_url="https://open.bigmodel.cn/api/paas/v4",  # Base URL for the API.
    max_retries=5,  # Maximum number of retry attempts for failed requests.
)

def generate_response(messages: List[Dict[str, str]]) -> str:
    """
    Generate a response from the model using the provided messages.

    Args:
        messages (List[Dict[str, str]]): A list of messages forming the conversation history.

    Returns:
        str: The response content from the model.
    """
    try:
        # Request a chat completion from the model.
        response = client.chat.completions.create(
            model="codegeex-4",  # Specify the model to use.
            messages=messages,  # Provide the conversation history.
            temperature=0,  # Set temperature for deterministic responses.
        ).choices[0].message.content  # Extract the content of the response message.
        
        # Ensure the response is not empty.
        assert response != ""
        return response
    except:
        # Return an empty string in case of an error.
        return ""

def parse_args():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Code Evaluation Tool")
    parser.add_argument('--model_name', type=str, required=True, help='Name of the model to use')
    parser.add_argument('--method_name', type=str, help='Name of the method to execute')
    parser.add_argument('--iterations', type=int, default=3, help='Number of iterations to perform')
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
