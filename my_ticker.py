#Stock Api Ticker

import requests
import configparser
import json
config = configparser.ConfigParser()
config.read("my_config.ini")
my_list = list()
for index in config["Tickers"]:
    my_list.append(config["Tickers"][index])
print (my_list)    
open("my_text.txt", "w").close()

for index in my_list  :  
    
    with open ("my_" + index + "_json.json", "wb") as my_file:
        response = (requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + index + "&apikey=EP35PLHWAS9L7GVC"))
        my_file.write(response.content)

    with open("my_" + index + "_json.json") as f:
        data = json.load(f)
    
        with open ("my_text.txt", "a") as my_file:
            my_file.write(data["Global Quote"]["01. symbol"])
            my_file.write("    ")
            my_file.write(data["Global Quote"]["05. price"])
            my_file.write("    ")
            my_file.write(data["Global Quote"]["10. change percent"])
            my_file.write("    ")

    