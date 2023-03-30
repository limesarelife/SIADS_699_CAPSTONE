import pandas as pd
import numpy as np
import requests
import time
from pytrends.request import TrendReq
import configparser

class fetch_trends:
    def __init__(self, path_file):
        self.path_file = path_file
    def get_trends(self):

        parser = configparser.ConfigParser()
        parser.read("cookie_config.txt")

        Cookies = parser.get("config", "CookieStrings")
        requests_args = {'headers' : {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
            'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': Cookies
        }
        }


    
        pytrends = TrendReq(tz=360, requests_args=requests_args,backoff_factor=2,retries=5)
        
        acnh_villagers= pd.read_csv(self.path_file + "villagers.csv")
        
        Villagers_list = acnh_villagers['Name'].to_list()
        
        villagers = []
        for item in Villagers_list:
            item = item + " Animal Crossing"
            villagers.append(item)
        # fixing OHare again to match
        acnh_villagers_two=["OHare Animal Crossing" if x=="O'Hare Animal Crossing" else x for x in villagers]

        kw_listed = acnh_villagers_two
        
        trends = dict()
        for i in kw_listed:
            print(i)
            ##build out query the code commented out was for original run in 2021 during Milestone 1
            pytrends.build_payload(kw_list=[i],timeframe='2020-03-20 2023-03-10')
            
            ##save trend to dictionary
            trends[i] = pytrends.related_queries()[i]

            # sleep to avoid 429 error 
            time.sleep(10)

        acnh_dict = dict()
        for item in acnh_villagers_two:
            i = trends[item]['rising']
            acnh_dict.update({item:i})
        
        print("good")
        return acnh_dict

    def convert_results(self, pytrend_dict):
        dict_list = []
        for key,value in pytrend_dict.items():
            if type(value) == pd.DataFrame:
                value['searchitem'] = key
                dict_list.append(value)
            else:
                dict_none = pd.DataFrame({"query":[np.nan],"value":[np.nan]})
                dict_none['searchitem'] = key
                dict_list.append(dict_none)
        
        # creating the final pytrends results to append to the villagers data in next script
        finalVillagerdf = pd.concat(dict_list, ignore_index = True)

        return finalVillagerdf.to_csv(self.path_file+"/final_pytrends.csv",index = False)

start_acnh_pytrends = fetch_trends("./python_villagers_create/")
trend_payloads = start_acnh_pytrends.get_trends()
print(trend_payloads)
final_trends = start_acnh_pytrends.convert_results(trend_payloads)
