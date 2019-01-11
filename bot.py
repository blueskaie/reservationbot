import argparse
import logging

from policy import RestaurantPolicy
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy
import requests
import wikipedia
logger = logging.getLogger(__name__)


class SearchAPI(object):
    def __init__(self):
        self.my_token =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.W3siX2lkIjp7IiRpZCI6IjViYzU0NzJlZGFjMDQ3YTdlNTVkYjU5ZCJ9LCJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIyMTIzMmYyOTdhNTdhNWE3NDM4OTRhMGU0YTgwMWZjMyIsInJvbGUiOiI1YzI1ZjY2MDZkNDk4ODAyMzgwYmJiMTciLCJlbWFpbCI6InN1cHBvcnRAdmFuaS5jb20iLCJjb3VudHJ5IjoiVVNBIiwiY2l0eSI6Ildhc2hpbmd0b24iLCJpc19kZWxldGUiOjAsImZpcnN0bmFtZSI6IkFkbWluIiwibGFzdG5hbWUiOiJBZG1pbiIsIm5vIjoiQTAwMDAwMDAwMDEiLCJ1cGRhdGVfYXQiOjE1Mzk3ODU0MTZ9XQ.hwESFiv7wUudcvHjWwNcDQlkexgifNg3t-_ghdHAvuo"
    
    def search_categories(self, ctype):
        print(ctype)
        print(self.my_token)
        try:
            response = requests.post("http://40.121.52.184:8088/vani-yasir/index.php/Api_controller/Category_by_type?type="+ctype+"&token="+self.my_token, data={'token':self.my_token, 'type':ctype})
            response = response.json()
            result = [{'title': item['name'], 'payload':'/inform{"category": "'+item['name']+'"}'} for item in response if 'name' in item]
            print(result)
            return result
        except:
            return []
    
    def search_subcategories(self, cname):
        print(cname)
        try:
            response = requests.post("http://40.121.52.184:8088/vani-yasir/index.php/Api_controller/Sub_category?name="+cname+"&token="+self.my_token)
            response = response.json()
            result = [{'title': item['name'], 'payload':'/inform{"sub_category": "'+item['name']+'"}'} for item in response if 'name' in item]
            print(result)
            return result
        except:
            return []

    def search_information(self, info):
        if info is None:
            return "I can't catch what you want(NLU ERROR)"
        try: 
            result = wikipedia.summary(info)
            return result
        except: 
            return "I can't find information about" + info

def train_dialogue(domain_file="restaurant_domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/babi_stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            RestaurantPolicy(batch_size=100, epochs=400,
                                             validation_split=0.2)])

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('data/nlu_data.md')
    trainer = Trainer(config.load("nlu_model_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")

    return model_directory

def run():
    from rasa_core.interpreter import RasaNLUInterpreter
    import time
    interpreter = RasaNLUInterpreter('models/nlu/default/current')
    messages = ["Hi! you can chat in this window. Type 'stop' to end the conversation."]
    agent = Agent.load('models/dialogue', interpreter=interpreter)

    print("I am bot for you")
    while True:
        time.sleep(0.3)
        a = input()
        if a == 'stop':
            break
        responses = agent.handle_text(a)
        for r in responses:
            res = r.get("text")
            if res:
                res = ">" + res
                print(res)

if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
        description='starts the bot')

    parser.add_argument(
        'task',
        choices=["train-nlu", "train-dialogue", "run"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()