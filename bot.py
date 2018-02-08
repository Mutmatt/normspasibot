import sys
import re
import time
import telepot
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

class MessageAnswer(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageAnswer, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        regex = re.compile('[^a-zA-Zа-яА-Я]')

        initialMessage = msg['text']
        msgText = initialMessage.lower().split(' ')

        filteredWords = list(map(lambda x: regex.sub('', x), msgText))

        #Ответ красное
        answersForRed = ["вопрос", "вопросик", "совет", "советик", "помощь", "помогите", "помогайте", "поможете", "проблему", "проблема", "проблемка", "проблемку", "посоветоваться", "посоветуйте"]
        if len(msgText) >= 2 and len(msgText) < 7 and any(filteredWords[-1] == word for word in answersForRed):
            self.sender.sendMessage("красное")
            print(datetime.now(), ": RED on ", msgText, " from ", msg['from']['username'], "")
            return

        #Ответ на как
        if any("как" == word for word in filteredWords):
            self.sender.sendMessage("нормально, спасибо")
            print(datetime.now(), ": NORM on ", msgText, " from ", msg['from']['username'], "")
            return

        #Ответ на нормально
        if any("нормально" == word for word in filteredWords):
            self.sender.sendMessage("спасибо")
            print(datetime.now(), ": SPASIB on ", msgText, " from ", msg['from']['username'], "")
            return

        #Ответ на пока
        if any("пока" == word for word in filteredWords):
            self.sender.sendMessage("ну пока")
            print(datetime.now(), ": NU_POKA on ", msgText, " from ", msg['from']['username'], "")
            return

        #Ответ на не понимаю, кто понимает, не могу понять, не понять
        if any("поним" or "понятн" in word for word in filteredWords) and any("не" == word for word in filteredWords):
            self.sender.sendMessage("ты просто не можешь понять")
            print(datetime.now(), ": PONYAL on ", msgText, " from ", msg['from']['username'], "")
            return

        #Ответ на вопрос с инфинитивом
        if "?" in initialMessage:
            firstWord = msgText[0]
            if (firstWord.endswith("ть") or firstWord.endswith("ться") or firstWord.endswith("ти")):
                self.sender.sendMessage("давай")
                print(datetime.now(), ": DAVAI on ", msgText, " from ", msg['from']['username'])
                return


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageAnswer, timeout=10
    ),
])
MessageLoop(bot).run_as_thread()

while 1:
	time.sleep(10)