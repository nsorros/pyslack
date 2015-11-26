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

def marshall(channel_name):
	marshaller = {
		'group': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members']},
		'channel': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members']},
		'im': lambda x: {'name': users[x['user']], 'id': x['id'], 'members': [x['user']]},
		'users': lambda x: {'name': x['name'], 'id': x['id']}
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
	slack_users = map(marshall("users"), get_list("users"))
	slack_bot = [{'id': 'USLACKBOT', 'name': 'slackbot'}]
	return {user['id']: user['name'] for user in slack_users + slack_bot}

def get_stars():
	return get_list("stars")

def display_channels(channels):
	for channel in channels:
		print "    {name}".format(name=channel['name'])

if __name__ == '__main__':
	users = get_users()
	channels = get_channels()
	stars = get_stars()

	is_starred_channel = lambda x: x['id'] in map(lambda x: x['channel'], filter(lambda x: x['type'] in ['im', 'group', 'channel'], stars))
	starred_channels = filter(is_starred_channel, channels)
	display_channels(starred_channels)
	


