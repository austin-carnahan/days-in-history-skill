import re
import wikipedia as wiki
from datetime import date
import locale
import random
from mycroft.util import extract_datetime

from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder


class TodayInHistory(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('TodayInHistoryIntent').
                    require("TodayInHistoryKeyword"))
    def handle_today_in_history_intent(self, message):
        if self.lang[:-3] == 'eu':
            locale.setlocale(locale.LC_TIME, "eu_ES.utf8")
        day_query = extract_datetime(message.data.get("utterance"))

        if not day_query:
            day_query = date.today().strftime("%B %d")
        else:
            day_query = day_query[0].strftime("%B %d")
        if self.lang[:-3] == 'eu':
            day_query = day_query[0].upper() + day_query[1:].replace(' ', 'k ')
        self._search(day_query)

    @intent_handler(IntentBuilder("TellMeMoreIntent").
                    require("TellMeMoreKeyword").require("initial_response"))
    def handle_tell_me_more_intent(self, message):
        """ Handler for follow-up inquiries 'tell me more'

            enabled after initial response is complete
        """

        if not self.events_list:
            self.speak_dialog("thatsall")
        else:
            events_list = self.events_list
            day = self.day

            selection_index = random.randrange(len(events_list))
            selected_event = events_list[selection_index]

            selected_event = day + ", " + selected_event
            self.speak(selected_event)

            events_list.pop(selection_index)
            self.events_list = events_list

    def _search(self, day_query):
        """ Searches wikipedia for an entry about a given day and replies to user
            Arguments:
                day_query: a string referencing a calendar day
                e.g. "March 15" or "May 6th"
        """
        try:

            # let the user know we're looking
            self.speak_dialog("searching", {"day": day_query})

            # get the wikipedia article for the chosen day
            # wiki.page will accept a range of day formats
            # including "August 5", "August 5th", and "5th of August"
            if self.lang[:-3] == 'eu':
                wiki.set_lang("eu")
            results = wiki.page(day_query)

            # remove irrelevant content so we are just looking at events
            if self.lang[:-3] == 'eu':
                events_string = 'Gertaerak'
            else:
                events_string = 'Events'
            events = re.search(r'(?<=' + events_string + ' ==\n).*?(?=\n\n\n==)',
                               results.content, re.DOTALL).group()

            # remove words between parenthesis and brackets for better speech
            # these are often birth/death days and less relevant asides.
            events = re.sub(r'\([^)]*\)|/[^/]*/', '', events)

            # parse results into a list.
            # Entries are seperated by newline characters
            str_list = re.split(r'\n', events)
            events_list=[x for x in str_list if x != '']
            for x in events_list:
                if x=="" or "=====" in x:
                    events_list.remove(x)

            # choose a random entry from the list
            selection_index = random.randrange(len(events_list))
            selected_event = events_list[selection_index]

            # a little string concatenation for clarity
            # right now our selection only contains a year
            self.speak(day_query + ", " + selected_event)

            # remove spoken entries and save data for further inquiry.
            # Flag initial response as complete to enable 'Tell Me More'
            # this doesn't work with bool'True'.... wants a string
            events_list.pop(selection_index)
            self.events_list = events_list
            self.day = day_query
            self.set_context("initial_response", "complete")

        except wiki.exceptions.PageError:
            self.speak_dialog("notfound")

        except wiki.exceptions.WikipediaExeption:
            self.speak_dialog("somethingwrong")

        except Exception as e:
            self.log.error("Error: {0}".format(e))

    def stop(self):
        pass


def create_skill():
    return TodayInHistory()
