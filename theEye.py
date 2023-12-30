from datetime import datetime
import json
import pytz


class Messages:
    def __init__(self):
        self.conversation: list[Message] = []
    def add(self, message):
        self.conversation.append(message)
    def display(self):
        for message in self.conversation:
            print(message.sender_name, message.timestamp_ms, message.type, message.content)
            
                
    def transcode_latin1_to_utf8(self):
        for i in range(len(self.conversation)):
            message = self.conversation[i]

            if message.type != 'content':
                continue
                
            transcoded_message = message.content.encode('latin_1').decode('utf-8')
            message.content = transcoded_message

    def change_timestamp_format(self):
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            timestamp_milliseconds = message.timestamp_ms
            timestamp_seconds = timestamp_milliseconds / 1_000
            dt_object = datetime.utcfromtimestamp(timestamp_seconds)
            
            # Apply timezone offset
            timezone_offset = -2
            dt_object_with_tz = dt_object.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(f'Etc/GMT{timezone_offset:+}'))
            
            iso8601_date = dt_object_with_tz.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + dt_object_with_tz.strftime('%Z:00')
            message.timestamp_ms = iso8601_date

    
class Message:
    def __init__(self, sender_name, timestamp_ms, type, content):
        self.sender_name = sender_name
        self.timestamp_ms = timestamp_ms
        self.type = type
        self.content = content

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.loads(file.read())
    return data


out = read_json_file('message_1.json')

messages = Messages()
for i in range(len(out.get('messages'))):
    message = out.get('messages')[i]
    keys_list = list(message.keys())
    messages.add(Message(message.get('sender_name'), message.get('timestamp_ms'), keys_list[2], message.get(str(keys_list[2]))))

messages.transcode_latin1_to_utf8()
messages.change_timestamp_format()

messages.display()