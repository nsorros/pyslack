import requests
import json
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

def marshall(channel_type):
	marshaller = {
		'group': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members'], 'type': 'groups'},
		'channel': lambda x: {'name': x['name'], 'id': x['id'], 'members': x['members'], 'type': 'channels'},
		'im': lambda x: {'name': users[x['user']]['name'], 'id': x['id'], 'members': [x['user']], 'type': 'im'},
		'users': lambda x: {'name': x['name'], 'id': x['id']},
		'stars': lambda x: {'id': x.get('channel')}
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
	human_users = map(marshall("users"), get_list("users"))
	bot_users = [{'id': 'USLACKBOT', 'name': 'slackbot'}]
	users = human_users + bot_users
	return users

def get_stars():
	stars = map(marshall("stars"), get_list("stars"))
	return stars

if __name__ == '__main__':

	with open('data/users.json', 'w') as f:
		users = {user['id']: user for user in get_users()}
		f.write(json.dumps({'data': users}))

	with open('data/channels.json', 'w') as f:
		channels = {channel['name']: channel for channel in get_channels()}
		f.write(json.dumps({'data': channels}))

	with open('data/stars.json', 'w') as f:
		stars = [star['id'] for star in get_stars()]
		f.write(json.dumps({'data': stars}))
