import os
import glob

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_spelling",
        "description": "Use this when the user wants to check the spelling of a name in a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the file to read"},
            },
            "required": ["path"]
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "fix_spelling",
        "description": "Use this as a reference for the correct spellings.The Correct spellings for for trust3.txt are Jeffrey Whitcombe, Katherine McLaughlin, Steven Pritchard, Elizabeth Carrington, Nicholas Fitzpatrick, Madeleine Harrington, and Christopher Beauregard.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. only .txt"},
                "content": {"type": "string", "description": "the content of the file"}
            },
            "required": ["path", "content"]
        }
    }
}

def agent(messages):
    tools = [
        read_file_tool_schema, write_file_tool_schema
    ]

    payload = {
        "model": "gpt-oss:20b",
        "messages": messages,
        "stream": False,
        "tools": tools
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    message = data["message"]
    return message

tool_called = True
messages = [
    {"role": "user", 
     "content": "I have a file named trust3.txt. I want to check the spelling of all the names in the document. Please list all the names. If you find any misspelled names, please provide a list of the misspelled names and their correct spelling. Then in a new document named updated_trust3.txt please correct the incorrectspelling of the names from trust3.txt and save the corrected document to updated_trust3.txt."}
]
while tool_called:
    message = agent(messages)
    print(message)
    tool_called = "tool_calls" in message

    if tool_called:
        print("tool called!")
        tool_calls = message["tool_calls"]
        tool_call = tool_calls[0]

        function_name = tool_call["function"]["name"]
        function_arguments = tool_call["function"]["arguments"]

        if function_name == "check_spelling":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "fix_spelling":
            content = function_arguments["content"]
            path = "updated_trust3.txt"
            with open(path, "w") as file:
                file.write(content)
            output = f"corrected document created: {path}"
            print(output)

        tool_message = {
            "role": "tool",
            "content": f"The output of tool {function_name} is: {output}"
        }
        messages.append(tool_message)
    else:
        ai_message = {
            "role":  message["role"],
            "content": message["content"]
        }
        messages.append(ai_message)

last_message = messages[-1]
import pprint
printer = pprint.pprint

printer(messages)

read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_dates",
        "description": "Use this when the user wants to check the dates in a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the file to read"},
            },
            "required": ["path"]
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "fix_dates",
        "description": "Use this as a reference for the correct date.The Correct date for for trust3.txt is June 29, 2023.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. only .txt"},
                "content": {"type": "string", "description": "the content of the file"}
            },
            "required": ["path", "content"]
        }
    }
}

def agent(messages):
    tools = [
        read_file_tool_schema, write_file_tool_schema
    ]

    payload = {
        "model": "gpt-oss:20b",
        "messages": messages,
        "stream": False,
        "tools": tools
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    message = data["message"]
    return message

tool_called = True
messages = [
    {"role": "user", 
     "content": "I have a file called updated_trust3.txt. I want to check the datess in the document. Please list all the dates. If you find any incorrect dates, please provide a list of the incorrect dates and the correct versions. Then in the document named updated_trust3.txt save the corrected dates and the corrected names."}
]
while tool_called:
    message = agent(messages)
    print(message)
    tool_called = "tool_calls" in message

    if tool_called:
        print("tool called!")
        tool_calls = message["tool_calls"]
        tool_call = tool_calls[0]

        function_name = tool_call["function"]["name"]
        function_arguments = tool_call["function"]["arguments"]

        if function_name == "check_dates":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "fix_dates":
            content = function_arguments["content"]
            path = "updated_trust3.txt"
            with open(path, "w") as file:
                file.write(content)
            output = f"corrected document created: {path}"
            print(output)

        tool_message = {
            "role": "tool",
            "content": f"The output of tool {function_name} is: {output}"
        }
        messages.append(tool_message)
    else:
        ai_message = {
            "role":  message["role"],
            "content": message["content"]
        }
        messages.append(ai_message)

last_message = messages[-1]
import pprint
printer = pprint.pprint

printer(messages)