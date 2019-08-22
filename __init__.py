import re
import wikipedia as wiki
from datetime import date
import random

from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder


class TodayInHistory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
  
    @intent_handler(IntentBuilder('TodayInHistoryIntent').require("TodayInHistoryKeyword"))
    def handle_today_in_history_intent(self, message):
        day_query = date.today().strftime("%B %d")

        self._search(day_query)

    @intent_handler(IntentBuilder("TellMeMoreIntent").require("TellMeMoreKeyword").require("initial_response"))
    def handle_tell_me_more_intent(self, message):
        """ Handler for follow-up inquiries 'tell me more'

        """

        if not self.events_list:
            self.speak("That's all the information I can find.")
        else:
            events_list = self.events_list
            day = self.day
            
            # choose a random entry from the list
            selection_index = random.randrange(len(events_list))
            selected_event = events_list[selection_index]

            # a little string concatenation for clarity. right now our selection only contains a year
            selected_event = day + ", " + selected_event
            self.speak(selected_event)

            # remove spoken entries and save data for further inquiry
            events_list.pop(selection_index)
            self.events_list = events_list


    def _search(self, day_query):
        """ Searches wikipedia for an entry about a given day and replies to user
            Arguments:
                day_query: a string referencing a calendar day e.g. "March 15" or "May 6th"
        """
        try:

            # let the user know we're looking
            self.speak_dialog("searching", {"day": day_query})

            # get the wikipedia article for the chosen day
            # wiki.page will accept a range of day formats including "August 5", "August 5th", and "5th of August"
            results = wiki.page(day_query)

            # prune away irrelevant content so we are just looking at events
            events = re.search(r'(?<=Events ==\n).*?(?=\n\n\n==)', results.content, re.DOTALL).group()

            # remove words between parenthesis and brackets for better speech
            # these are often birth/death days and less relevant asides.
            events = re.sub(r'\([^)]*\)|/[^/]*/', '', events)

            # parse results into a list
            events_list = re.split(r'\n', events)

            # choose a random entry from the list
            selection_index = random.randrange(len(events_list))
            selected_event = events_list[selection_index]

            # a little string concatenation for clarity. right now our selection only contains a year
            selected_event = day_query + ", " + selected_event
            self.speak(selected_event)

            # remove spoken entries and save data for further inquiry
            events_list.pop(selection_index)
            self.events_list = events_list
            self.day = day_query
            self.set_context("initial_response", "complete")

            
        except:
            pass

    def stop(self):
        pass


def create_skill():
    return TodayInHistory()

