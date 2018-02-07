import sys
import time
import telepot
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

class MessageAnswer(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageAnswer, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
    	msgText = msg['text'].lower()

    	#Ответ на текст с как
    	if "как " in msgText or msgText.endswith(" как"):
    		self.sender.sendMessage("нормально, спасибо")
    		print(datetime.now(), ": NORM on ", msgText, " from ", msg['from']['username'], "")

    	#Ответ на вопрос с почему
    	pochemus = ("почему ", " почему", "почему")
    	if any(x in msgText for x in pochemus):
    		self.sender.sendMessage("так вышло")
    		print(datetime.now(), ": TAK VISHLO on ", msgText, " from ", msg['from']['username'])

    	#Ответ на вопрос с инфинитивом
    	if "?" in msgText:
    		firstWord = msgText.partition(' ')[0].replace("?", "")
    		if (firstWord.endswith("ть") or firstWord.endswith("ться")):
	    		self.sender.sendMessage("давай")
	    		print(datetime.now(), ": DAVAI on ", msgText, " from ", msg['from']['username'])


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageAnswer, timeout=10
    ),
])
MessageLoop(bot).run_as_thread()

while 1:
	time.sleep(10)