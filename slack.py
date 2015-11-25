import requests
import os

SLACK_API='https://slack.com/api'
SLACK_TOKEN = os.environ['SLACK_TOKEN']


slack_list_name = {
	'groups': 'groups',
	'channels': 'channels',
	'im': 'ims',
	'users': 'members',
}

def marshall(channel_name):
	marshaller = {
		'group': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members']},
		'channel': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members']},
		'im': lambda x: {'name': x['user'], 'id': x['id'], 'members': [x['user']]},
	}
	return marshaller[channel_name]

def get_list(list_name):
	url = "{api}/{name}.list".format(api=SLACK_API, name=list_name)
	params = {
		'token': SLACK_TOKEN,
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
	slack_users = get_list("users")
	pass

def get_stars():
	return get_list("stars")

def display_channels(channels):
	for channel in channels:
		print "    {name}".format(name=channel['name'])

if __name__ == '__main__':
	channels = get_channels()
	stars = get_stars()
	users = get_users()

	is_starred_channel = lambda x: x['id'] in map(lambda x: x['channel'], filter(lambda x: x['type'] in ['im', 'group', 'channel'], stars))
	starred_channels = filter(is_starred_channel, channels)
	display_channels(starred_channels)
	


