from datetime import datetime
import json
import pytz

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

def change_timestamp_format(conversation):
    for i in range(len(conversation.get('messages'))):
        message = conversation.get('messages')[i]
        timestamp_milliseconds = message.get('timestamp_ms')
        timestamp_seconds = timestamp_milliseconds / 1_000
        dt_object = datetime.utcfromtimestamp(timestamp_seconds)
        
        # Apply timezone offset
        timezone_offset = -2  # Replace with your desired timezone offset
        dt_object_with_tz = dt_object.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(f'Etc/GMT{timezone_offset:+}'))
        
        iso8601_date = dt_object_with_tz.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + dt_object_with_tz.strftime('%Z:00')
        message.update({'timestamp_ms': iso8601_date})
    return conversation

out = read_json_file('message_1.json')

out = transcode_latin1_to_utf8(out)

out = change_timestamp_format(out)
    
print(out.get('messages')[0])