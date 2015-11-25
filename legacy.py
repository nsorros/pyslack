def inbox(user):
	url = "{api}/{endpoint}".format(
		api=SLACK_API,
		endpoint=MESSAGES_ENDPOINT)
	params = {
		'token': SLACK_TOKEN,
		'channel': user['channel']
	}
	response = requests.get(url, params)
	if response.status_code == 200:
		return response.json()['messages']
	return []

def display(messages):
	for message in sorted(messages, key=lambda x: x['ts']):
		sender = "Aris" if message['user'] == aris['id'] else "Nick"
		print "{} {}".format(sender, message['text'].encode('ascii', 'ignore'))

def send_reply(user, reply):
	url = "{api}/{endpoint}".format(
		api=SLACK_API,
		endpoint=REPLY_ENDPOINT)
	params = {
		'token': SLACK_TOKEN,
		'channel': user['channel'],
		'text': reply,
		'as_user': 'true'
	}
	requests.post(url, params)

def chat(user):
	user_messages = inbox(user)
	display(user_messages)
	reply = raw_input('Send: ')
	if reply:
		send_reply(user, reply)

def home():
	# while True:
		# check if there are new messages
		# display all saved channels and number of unread
		# wait for input for 10 sec
	pass

def channel_info(channel):
	url = "https://slack.com/api/channels.info"
	params = {
		'token': SLACK_TOKEN,
		'channel': channel
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()['channel']['name']
	return

def im_history(channel):

	url = "https://slack.com/api/im.history"
	params = {
		'token': SLACK_TOKEN,
		'channel': channel
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()['messages']['name']
	return

def group_info(channel):
	url = "https://slack.com/api/groups.info"
	params = {
		'token': SLACK_TOKEN,
		'channel': channel
	}
	response = requests.get(url, params)
	if response.status_code == 200 and 'error' not in response.json():
		return response.json()['group']['name']
	return