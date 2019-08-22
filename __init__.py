import re
import wikipedia as wiki
from datetime import date

from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder


class TodayInHistory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
  
    @intent_handler(IntentBuilder('TodayInHistoryIntent').require("TodayInHistoryKeyword"))
    def handle_today_in_history_intent(self, message):
        day_query = date.today().strftime("%B %d")

        self._lookup(day_query)

    def _lookup(self, day_query):
        """ Searches wikipedia for an entry about a given day and replies to user
            Arguments:
                day_query: a string referencing a calendar day e.g. "March 15" or "May 6th"
        """
        try:
            self.speak_dialog("searching", {"day": day_query})

        except:
            pass

    def stop(self):
        pass


def create_skill():
    return TodayInHistory()

