import ast
import os
import sys
import openai
import requests
import json
from dotenv import load_dotenv
# Set up your OpenAI API credentials

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_gpt3_5_response(messages: list):
    # Todo: Optimize below hyper-parameters.
    print("Inside get_gpt3_5_response")
    print(messages)
    request_body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0,
        "top_p": 0
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    openai_chat_completion_url = "https://api.openai.com/v1/chat/completions"
    text_completion_response = requests.post(url=openai_chat_completion_url, data=json.dumps(request_body),
                                             headers=headers, timeout=60)

    print(f"text_completion_response: {text_completion_response}")
    if text_completion_response.status_code != 200:
        return "Openai API response error"
    else:
        return text_completion_response.json().get("choices")[0].get("message").get("content")


def generate_description(function_source):
    # Generate a description for the given function using GPT-3.5
    prompt = f"Describe the following function in one line:\n\n{function_source}\n\n"

    # Extract the generated description from the API response
    description = get_gpt3_5_response(messages=[{
                "role": "system",
                "content": prompt
            }])

    return description


def add_descriptions_to_functions(file_name):
    with open(file_name, 'r') as file:
        content = file.read()

    # Parse the file's AST (Abstract Syntax Tree)
    tree = ast.parse(content)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)

    # Update the file with descriptions
    with open(file_name, 'r') as file:
        lines = file.readlines()

    count = 0
    for function in functions:
        start_lineno = function.lineno + count
        end_lineno = function.body[-1].lineno

        count = count + 1

        function_source = ast.unparse(function).strip()
        description = generate_description(function_source)

        # Insert the generated description beneath the function
        description_lines = ['    """' + description + '"""\n']
        lines.insert(start_lineno, description_lines[0])

    # Write the updated content back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python program.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    add_descriptions_to_functions(file_name)