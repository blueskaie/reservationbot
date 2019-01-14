## story_order_1
* greet
 - utter_ask_help
* needorderhelp
 - action_search_categories
 - action_suggest
* inform{"category": "product"}
 - action_search_subcategories
 - action_suggest
* inform{"sub_category": "product"}
 - action_search_products
 - action_suggest
* inform{"product": "tomato"}
 - utter_ask_numunits
* inform{"quantity": "1"}
 - utter_ask_ordermore
* deny
 - utter_ack_login
* login
 - utter_ask_credential
* inform{"username": "admin", "password": "admin"}
 - utter_ack_makereservation
* thankyou
 - utter_goodbye

## story_information_2
* greet
 - utter_ask_help
* needinformationhelp
 - utter_ask_information
* requestinfo{"info": "product"}
 - action_search_information
 - action_suggest_text
 - utter_ask_satisfaction
* affirm
 - utter_goodbye

 ## story_information_3
* greet
 - utter_ask_help
* needinformationhelp
 - utter_ask_information
* requestinfo{"info": "product"}
 - action_search_information
 - action_suggest_text
 - utter_ask_satisfaction
* thankyou
 - utter_goodbye