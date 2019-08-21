from mycroft import MycroftSkill, intent_file_handler
from adapt.intent import IntentBuilder


class TodayInHistory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        today_in_history_intent = IntentBuilder("TodayInHistoryIntent").require("TodayInHistoryKeyword").build()
        self.register_intent(today_in_history_intent, self.handle_today_in_history_intent)
        
    #~ @intent_file_handler('today.in.history.intent')
    def handle_today_in_history_intent(self, message):
        self.speak_dialog('searching')

    def stop(self):
        pass


def create_skill():
    return TodayInHistory()

