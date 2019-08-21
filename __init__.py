from mycroft import MycroftSkill, intent_file_handler


class DaysInHistory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('history.in.days.intent')
    def handle_history_in_days(self, message):
        self.speak_dialog('history.in.days')


def create_skill():
    return DaysInHistory()

