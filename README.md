# Messenger Messages Analyzer

This project analyzes Facebook Messenger messages and provides insights such as word distribution, message counts by person, and message counts by hour and day.

## Usage

1. Ensure you have the necessary JSON files containing Messenger messages. It can be requested via Facebook https://accountscenter.facebook.com/info_and_permissions
2. Update the file paths in the script if necessary.
3. Run the script:

```bash
python messenger_messages_analyzer.py
```

## Features

- Message Transcoding: Converts Latin-1 encoded messages to UTF-8.
- Timestamp Formatting: Changes the timestamp format to ISO 8601 with timezone offset.
- Word Distribution Analysis: Analyzes word distribution in messages and plots the most popular words.
- Message Counts: Calculates the number of messages by person, hour, and day.
- Saving Messages: Saves the analyzed messages to a TSV file for further analysis.
