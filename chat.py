import requests
import os

SLACK_API = 'https://slack.com/api'
SLACK_TOKEN = os.environ['SLACK_TOKEN']


def send(channel, message):
	url = "{api}/chat.postMessage".format(api=SLACK_API)
	params = {
		'token': SLACK_TOKEN,
		'channel': channel['id'],
		'text': message,
		'as_user': 'true'
	}
	requests.post(url, params)