from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from bot import SearchAPI
from typing import Dict, Text, Any, List, Union

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

class ActionSearchProducts(Action):
    def name(self):
        return 'action_search_products'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        sub_products = myapi.search_products(tracker.get_slot("sub_category"))
        
        return [SlotSet("suggest_buttons", sub_products)]


class ActionSearchInformation(Action):
    def name(self):
        return 'action_search_information'

    def run(self, dispatcher, tracker, domain):
        myapi = SearchAPI()
        searchkey = tracker.latest_message
        print(searchkey)
        result = myapi.search_information(searchkey)
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
            dispatcher.utter_button_message("Sure, What are you looking for?", suggest_buttons)
        else:
            dispatcher.utter_message("I can't find what you want")
        return []

class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "restaurant_form"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""

        return ["test1", "test2"]

    def slot_mapping(self):
        # type: () -> Dict[Text: Union[Text, Dict, List[Text, Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where the first match will be picked"""

        return {"test1": [self.from_entity(entity="test1"),
                         self.from_text()],
                "test2": [self.from_entity(entity="test1"),
                         self.from_text()]}

    def submit(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []