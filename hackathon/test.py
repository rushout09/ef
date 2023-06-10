import requests
import json
import os
from dotenv import load_dotenv
# Set up your OpenAI API credentials

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API credentials

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def extract_functions(code):
    functions = []
    lines = code.split("\n")
    current_function = ""
    for line in lines:
        line = line.strip()
        if line.startswith("def"):
            if current_function:
                functions.append(current_function)
            current_function = line
        elif current_function:
            current_function += "\n" + line
    if current_function:
        functions.append(current_function)
    return functions

def get_gpt3_5_response(messages: list):
    request_body = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    openai_chat_completion_url = "https://api.openai.com/v1/chat/completions"
    text_completion_response = requests.post(url=openai_chat_completion_url, data=json.dumps(request_body),
                                             headers=headers, timeout=60)

    text_completion_json = text_completion_response.json()
    choices = text_completion_json.get("choices")
    if choices:
        text_completion = choices[0].get("message").get("content")
        return text_completion
    else:
        return None


file_path = 'app.py'
code = read_code_from_file(file_path)
functions = extract_functions(code)

for function in functions:
    if function.startswith("def"):
        function_name = function.split("def ")[1].split("(")[0]
        module_name="hackathon.app "
        unit_test_file_name = f"unit_test_{function_name}.py"

        with open(unit_test_file_name, 'w') as file:
            user_input = function
            messages = [
                {
                    "role": "system",
                    "content": "Generate only the unit test for the function: {} in the module: {}, ensuring it is semantically valid Python code. Use only the available data within the function and be deterministic, without imagining anything.".format(function_name, module_name)
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            response = get_gpt3_5_response(messages=messages)
            if response:
                file.write(response + '\n')
            else:
                file.write("Error: No response from the API\n")