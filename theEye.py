import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.loads(file.read())
    return data

def transcode_latin1_to_utf8(conversation):
    for i in range(len(conversation.get('messages'))):
        message = conversation.get('messages')[i]

        if 'content' not in message:
            continue
            
        transcoded_message = message.get('content').encode('latin_1').decode('utf-8')
        message.update({'content': transcoded_message})
    return conversation

def print_json_structure(data, indent=2):
    def explore_structure(obj, current_indent):
        if isinstance(obj, dict):
            for key, value in obj.items():
                print(" " * current_indent + f'"{key}":')
                explore_structure(value, current_indent + indent)
        elif isinstance(obj, list):
            for item in obj:
                explore_structure(item, current_indent + indent)

    explore_structure(data, 0)

out = read_json_file('message_1.json')

print(print_json_structure(out))

out = transcode_latin1_to_utf8(out)
    
# print(out.get('messages'))