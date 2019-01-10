from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from bot import SearchAPI


class ActionSearchCategories(Action):
    def name(self):
        return 'action_search_categories'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        categories = myapi.search_categories(tracker.get_slot("type"))
        
        return [SlotSet("matches", categories)]

class ActionSearchSubCategories(Action):
    def name(self):
        return 'action_search_subcategories'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        sub_categories = myapi.search_subcategories(tracker.get_slot("category"))
        
        return [SlotSet("matches", sub_categories)]

class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        matches = tracker.get_slot("matches")
        if matches:
            dispatcher.utter_button_message("What do you want among them?", matches)
        else:
            dispatcher.utter_message("I can't find what you want")
        return []