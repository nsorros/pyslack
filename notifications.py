import requests
import os

SLACK_API = 'https://slack.com/api'
SLACK_TOKEN = os.environ['SLACK_TOKEN']


def get_history(channel):
	url = "{api}/{channel_type}.history".format(api=SLACK_API, channel_type=channel['type'])
	params = {
		'token': SLACK_TOKEN,
		'channel': channel['id'],
		'count': 10,
		'unreads': 1
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()
	return {}

def get_unread_messages(channel):
	history = get_history(channel)
	unread_count = history['unread_count_display']
	unreads = [
		message
		for message in history['messages'][:unread_count+1]
	]
	return unreads

def unread_messages(channels):
	messages = [
		{
			'text': message['text'],
			'channel': channel['name']
		}
		for channel in channels
		for message in get_unread_messages(channel)
	]
	return messages
