import sys

if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		# notifications
		print("Nothing new")
		exit

	if len(sys.argv) == 2:
		# send message to user in argument
		# ask user what message to send
		channel = sys.argv[1]
		message = raw_input("#{channel}: ".format(channel=channel))
		print "send"
		exit

	if len(sys.argv) > 2:
		channel = sys.argv[1]
		message = " ".join(sys.argv[2:])
		# send message to channel
		print "send to #{channel}".format(channel=channel)
		exit

