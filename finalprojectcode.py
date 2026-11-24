import os
import glob

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_content",
        "description": "Use this when the user wants to read the entire contents of a .txt file. Read both the original document and the correctcontents.txt so the orginal document can be corrected in a new file using the information in the reference file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the file to read"},
            },
            "required": ["path"]
        }
    }
}

list_files_schema = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Use this when the user wants to list files in the current working directory by default, or in a named directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the directory on which to list the files."}
            },
            "required": []
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "fix_content",
        "description": "Use this when the user wants to create a new file containing the entire original document with all of the spelling and date corrections incorporated.",
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
        read_file_tool_schema, list_files_schema, write_file_tool_schema
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
     "content": "Use the entire will5.txt and correct all the mispelled names and incorrect dates using correctcontents.txt. Compare the names and dates in the orginal document agaisnt the reference file. Then reproduce the entire will5.txt with the corrections in one new file with a name that has not been used before. Do not shorten the original document."}
]
while tool_called:
    message = agent(messages)
    print(message)
    tool_called = "tool_calls" in message

    if tool_called:
        print("tool called!")

        messages.append(message)

        tool_calls = message["tool_calls"]
        
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            function_arguments = tool_call["function"]["arguments"]

        if function_name == "check_content":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "list_files":
            path = "."
            if "path" in function_arguments:
                path = function_arguments["path"]
            print(f"arguments for list_files: {path}")
            files = glob.glob(f"{path}/*")
            output = files

        if function_name == "fix_content":
            content = function_arguments["content"]
            path = function_arguments ["path"]
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


