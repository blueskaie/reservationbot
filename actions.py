from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from bot import SearchAPI


class ActionSearchCategories(Action):
    def name(self):
        return 'action_search_categories'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        categories = myapi.search_categories("product")
        return [SlotSet("suggest_buttons", categories)]

class ActionSearchSubCategories(Action):
    def name(self):
        return 'action_search_subcategories'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        sub_categories = myapi.search_subcategories(tracker.get_slot("category"))
        
        return [SlotSet("suggest_buttons", sub_categories)]

class ActionSearchInformation(Action):
    def name(self):
        return 'action_search_information'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        result = myapi.search_information(tracker.get_slot("info"))
        # dispatcher.utter_message(result)
        return [SlotSet("suggest_text", result)]

class ActionSuggestText(Action):
    def name(self):
        return 'action_suggest_text'
    def run(self, dispatcher, tracker, domain):
        print("action_suggest_text")
        dispatcher.utter_message(tracker.get_slot("suggest_text"))

class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        print("action_suggest")
        suggest_buttons = tracker.get_slot("suggest_buttons")
        if suggest_buttons:
            dispatcher.utter_button_message("What do you want among them?", suggest_buttons)
        else:
            dispatcher.utter_message("I can't find what you want")
        return []