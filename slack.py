import json
import sys
import os

from notifications import get_unread_messages
from chat import send

SLACK_API = 'https://slack.com/api'
SLACK_TOKEN = os.environ['SLACK_TOKEN']

channels = json.load(open('data/channels.json'))['data']
users = json.load(open('data/users.json'))['data']
stars = json.load(open('data/stars.json'))['data']


if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		starred_channels = filter(lambda x: x['id'] in stars, channels.values())
		unread_messages = get_unread_messages(starred_channels)
		for message in unread_messages:
			print "  #{channel:20}: {text}".format(channel=message['channel'], text=message['text'][:60])
		if not unread_messages:
			print "  No messages. Business as usual."
		exit

	if len(sys.argv) == 2:
		channel_name = sys.argv[1]
		message = raw_input("#{channel_name}: ".format(channel_name=channel_name))
		channel = channels[channel_name]
		send(channel, message)
		print "send"
		exit

	if len(sys.argv) > 2:
		channel_name = sys.argv[1]
		message = " ".join(sys.argv[2:])
		channel = channels[channel_name]
		send(channel, message)
		print "send to #{channel_name}".format(channel_name=channel_name)
		exit

