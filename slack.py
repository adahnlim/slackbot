from slacker import Slacker
import websocket
import thread
import time
import json
import google


channel = '#general'
CMDCHAR='?'

CMD_LIST=['work','home','cal']

token = 'YOUR-TOKEN'


slack = Slacker(token)


def on_message(ws, message):
	

	msg =  json.loads(message)

	if msg['type'] == 'message':
		
		cmd = msg['text'].split(CMDCHAR)
			
		if msg['text'][0:1] == CMDCHAR:
			
			 
			if cmd[1] == "help":
				
				msg = [{
					'fallback':'HELP U',
					'pretext':'HELP U',
					'text':'Adahnbot Usage : ' + CMDCHAR + '{'+','.join(CMD_LIST)+'}\nAdahnbot Help : ' + CMDCHAR + 'help\n',
					'color':'#36a64f'		
				}]
				slack.chat.post_message(channel,'',attachments=msg,as_user=True)
			
			elif cmd[1] =="cal":
				slack.chat.post_message(channel,'Waiting...',as_user=True)
				msg = [{
					'fallback':'CALENDAR INFO',
					'pretext':'*CALENDAR INFO*',
					'text': '\n'.join(google.getCalendar()),
					'color':'#FF5E00',
					'mrkdwn_in':['pretext']
				}]
				
				slack.chat.post_message(channel,'',attachments=msg,as_user=True)

			# something else..
			#elif cmd[1] =="..":
				#pass

			else:
				pass
		


def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        time.sleep(1)

    thread.start_new_thread(run, ())



res =  slack.auth.test().body

msg = [{
			'fallback':res['user']+' is LOG-IN!',
			'pretext':'*Connected to ' +res['team']+'('+channel+')*',
			'text':'bot Usage : ' + CMDCHAR + '{'+','.join(CMD_LIST)+'}\nbot Help : ' + CMDCHAR + 'help',
			'color':'#36a64f',
			'mrkdwn_in':['pretext']
		}]


slack.chat.post_message(channel,'',attachments=msg,as_user=True)


response = slack.rtm.start()
endpoint = response.body['url']


#websocket.enableTrace(True)
ws = websocket.WebSocketApp(endpoint,on_message = on_message, on_error = on_error,on_close = on_close)
ws.on_open = on_open
ws.run_forever()   