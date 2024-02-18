from datetime import datetime
from io import TextIOWrapper
import json
import re
from typing import Any
from numpy import insert
import pytz
import plotly.graph_objects as go


NUMBER_OF_MESSAGES = 300

class Messages:
    def __init__(self):
        self.conversation: list[Message] = []
        self.names: list[str] = []

    def add_name(self, name):
        self.names.append(name)
    def add(self, message):
        self.conversation.insert(0, message)
    def display(self):
        for message in self.conversation:
            message.display()
            print("\n")
            
                
    def transcode_latin1_to_utf8(self):
        for i in range(len(self.conversation)):
            message = self.conversation[i]

            if message.type != 'content':
                continue
                
            transcoded_message = message.content.encode('latin-1').decode('utf-8')
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
            message.time_human_readable = iso8601_date

    def by_person_words_distribution(self, name) -> dict[str, int]:
        word_count = {}
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            if message.sender_name not in name:
                continue

            for iter, word in enumerate(message.split_words):
                if word == '':
                    print(f"{message.content}; '{message.split_words[iter-1]}'; '{message.split_words[iter]}'")
                    exit(1)
                word = word.lower()
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

        return word_count

    def plot_words_distribution(self, word_count, name):
        sorted_words_distribution = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        most_popular_word = sorted_words_distribution[0][0]
        print(name)
        print(f"Number of different occurrences: {len(sorted_words_distribution)}")
        num_of_messages = NUMBER_OF_MESSAGES
        if len(sorted_words_distribution) < NUMBER_OF_MESSAGES:
            num_of_messages = len(sorted_words_distribution)
        percentage_of_words = num_of_messages / len(sorted_words_distribution) * 100
        print(f"{num_of_messages} in terms of percentage_of_words {percentage_of_words}%")
        sorted_words_distribution = sorted_words_distribution[:num_of_messages]
        print(f"Most popular: '{most_popular_word}', value: {sorted_words_distribution[0][1]}")

        print()

        labels, values = zip(*sorted_words_distribution)
        labels = list(labels)
        if re.match(r'\d{4}-\d{2}-\d{2}', labels[0]):
            for i in range(len(labels)):
                    labels[i] = str(i+1) + '. ' + labels[i]        

        fig = go.Figure()

        # Add bar trace
        bar = go.Bar(
            x=labels,
            y=values,
            marker_color='blue',
            hoverinfo='y+text',
            text=labels,
            textfont=dict(size=20),  # Adjust text size
            insidetextanchor=None,
        )

        # Add the bar trace to the figure
        fig.add_trace(bar)

        # Update layout for better visualization
        fig.update_layout(
            title=f"{percentage_of_words}% most popular Words Distribution of {name}",
            xaxis_title='Categories',
            yaxis_title='Word Counts',
            hovermode='closest',  # Display the hover info of the nearest point
            showlegend=False,  # Hide legend for simplicity
            xaxis=dict(tickvals=[]),  # Hide x-axis tick labels
        )
        fig.show()
        return most_popular_word


    def find_by_date(self, date): #TODO: add surrounding days
        filtered_messages = []
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            if message.time_human_readable.split('T')[0] == date:
                filtered_messages.insert(0, message)
        return filtered_messages


            
    def split_words(self):
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            message.split_words = message.content.split()

    def number_of_messages_by_person(self):
        print("number_of_messages_by_person")
        number_of_messages_by_person = {}
        number_of_messages_by_person[str(messages.names)] = 0
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            if message.sender_name in number_of_messages_by_person:
                number_of_messages_by_person[message.sender_name] += 1
                number_of_messages_by_person[str(messages.names)] += 1
            else:
                number_of_messages_by_person[message.sender_name] = 1
        print(number_of_messages_by_person, "\n")
    
    def number_of_messages_by_day(self, name) -> dict[str, int]:
        number_of_messages_by_day = {}
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            if message.sender_name not in name:
                continue
            day = message.time_human_readable.split('T')[0]
            if day in number_of_messages_by_day:
                number_of_messages_by_day[day] += 1
            else:
                number_of_messages_by_day[day] = 1
        return number_of_messages_by_day
    
    def number_of_messages_by_hour(self, name)-> dict[str, int]:
        number_of_messages_by_hour = {}
        for i in range(len(self.conversation)):
            message = self.conversation[i]
            if message.type != 'content':
                continue
            if message.sender_name not in name:
                continue
            hour = message.time_human_readable.split('T')[1].split(':')[0]
            if hour in number_of_messages_by_hour:
                number_of_messages_by_hour[hour] += 1
            else:
                number_of_messages_by_hour[hour] = 1
        return number_of_messages_by_hour
    def show_words_distribution_for_each_person(self, method):
        print(method.__name__)
        most_popular = {}
        name = messages.names
        words_distribution = method(name)
        most_popular[str(name)] = messages.plot_words_distribution(words_distribution, name)
        words_distribution = method(name[0])
        most_popular[name[0]] = messages.plot_words_distribution(words_distribution, name[0])
        words_distribution = method(name[1])
        most_popular[name[1]] = messages.plot_words_distribution(words_distribution, name[1])
        return most_popular

    
class Message:
    def __init__(self, sender_name, timestamp_ms, type, content):
        self.sender_name = sender_name
        self.timestamp_ms = timestamp_ms
        self.time_human_readable = timestamp_ms
        self.type = type
        self.content: str = content
        self.split_words = []

    def display(self):
        for _, value in vars(self).items():
            print(value, end='\t')
    def save(self, file: TextIOWrapper):
        string = ""
        if self.type not in ['is_unsent']:
            if self.type == 'content':
                content = self.content.replace('\r\n', r' \\r\\n ')
                content = content.replace('\n', r' \n ')
            else:
                content = self.content
            string = f"{self.sender_name}\t{self.time_human_readable}\t{content}\n"
        file.write(string)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.loads(file.read())
    return data

def save_messages(messages: list[Message], file_name):
    with open(file_name, 'w') as file:
        for message in messages:
            message.save(file)


def read_multiple_json_files():
    out = Any
    for i in range(1, 6):
        data = read_json_file(f'message_{i}.json')
        if i == 1:
            out = data
        else:
            out.get('messages').extend(data.get('messages'))
    return out


out = read_multiple_json_files()

messages = Messages()
for i in range(len(out.get('messages'))):
    message = out.get('messages')[i]
    keys_list = list(message.keys())
    messages.add(Message(message.get('sender_name'), message.get('timestamp_ms'), keys_list[2], message.get(str(keys_list[2]))))

messages.add_name(out.get('participants')[0].get('name'))
messages.add_name(out.get('participants')[1].get('name'))

messages.transcode_latin1_to_utf8()
messages.change_timestamp_format()
messages.split_words()
messages.number_of_messages_by_person()
# messages.show_words_distribution_for_each_person(messages.by_person_words_distribution)

# most_popular_date = messages.show_words_distribution_for_each_person(messages.number_of_messages_by_day)
# most_popular_date = most_popular_date[str(messages.names)]
# by_date_filtered_messages = messages.find_by_date(most_popular_date)
# save_messages(by_date_filtered_messages, "filtered_messages.txt")
save_messages(messages.conversation, "all_messages.tsv")

# messages.show_words_distribution_for_each_person(messages.number_of_messages_by_hour)

