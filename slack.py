import requests
import os

SLACK_API='https://slack.com/api'
SLACK_TOKEN = os.environ['SLACK_TOKEN']


slack_list_name = {
	'groups': 'groups',
	'channels': 'channels',
	'im': 'ims',
	'users': 'members',
	'stars': 'items'
}

slack_info_name = {
	'groups': 'group',
	'channels': 'channel',
	'im': 'messages'
}

def get_info(channel_id, channel_type):
	url = "{api}/{channel_type}.info".format(api=SLACK_API, channel_type=channel_type)
	params = {
		'token': SLACK_TOKEN,
		'channel': channel_id,
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()[slack_info_name[channel_type]]
	return {}

def get_history(channel_id, channel_type):
	url = "{api}/{channel_type}.history".format(api=SLACK_API, channel_type=channel_type)
	params = {
		'token': SLACK_TOKEN,
		'channel': channel_id,
		'count': 1,
		'unreads': 1
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()
	return {}

def marshall(channel_type):
	marshaller = {
		'group': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members'], 'unread_count': get_info(x['id'], 'groups')['unread_count']},
		'channel': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members'], 'unread_count': get_info(x['id'], 'channels')['unread_count']},
		'im': lambda x: {'name': users[x['user']], 'id': x['id'], 'members': [x['user']], 'unread_count': get_history(x['id'], 'im')['unread_count_display']},
		'users': lambda x: {'name': x['name'], 'id': x['id']}
	}
	return marshaller[channel_type]

def get_list(list_name):
	url = "{api}/{name}.list".format(api=SLACK_API, name=list_name)
	params = {
		'token': SLACK_TOKEN,
		'exclude_archived': 1
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()[slack_list_name[list_name]]
	return []

def get_channels():
	"""
	returns [channel, ...]
		channel
			name:           string
			id:             string
			members:        [user_id, ...]
			unread count:   int
	"""
	channels = map(marshall("group"), get_list("groups")) + \
			   map(marshall("channel"), get_list("channels")) + \
			   map(marshall("im"), get_list("im"))
	return channels

def get_users():
	"""
	returns [user, ...]
		user
			name: string
			id:   string
	"""
	slack_users = map(marshall("users"), get_list("users"))
	slack_bot = [{'id': 'USLACKBOT', 'name': 'slackbot'}]
	return {user['id']: user['name'] for user in slack_users + slack_bot}

def get_stars():
	return get_list("stars")

def get_unread_count(channel):
	pass

def display_channels(channels):
	import random
	for channel in channels:
		print "    {name:20} *{unread_count}".format(name=channel['name'], unread_count=channel.get('unread_count', random.randint(0,4)))

if __name__ == '__main__':
	users = get_users()
	channels = get_channels()
	stars = get_stars()

	is_starred_channel = lambda x: x['id'] in map(lambda x: x['channel'], filter(lambda x: x['type'] in ['im', 'group', 'channel'], stars))
	starred_channels = filter(is_starred_channel, channels)
	display_channels(starred_channels)
	


