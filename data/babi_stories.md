## story_00914561
* greet
 - utter_ask_category
* inform{"type": "product"}
 - utter_ack_dosearch
 - action_search_categories
 - action_suggest
* inform{"category": "product"}
 - utter_ack_dosearch
 - action_search_subcategories
 - action_suggest
* inform{"sub_category": "product"}
 - utter_ack_makereservation
* thankyou
 - utter_goodbye
