import pandas as pd
import matplotlib as plot
import numpy as np
import time
#import pytrends
from pytrends.request import TrendReq
# pytrend = TrendReq(hl='en-US', tz=360)

class fetch_trends:
    def __init__(self, path_file):
        self.path_file = path_file
    def get_trends(self):
        # pytrend = TrendReq(hl='en-US', tz=360)
        requests_args = {'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        }
        
        # pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=1, requests_args={'verify':False})
        pytrends = TrendReq(hl='en-US', tz=360, requests_args=requests_args)
        
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
            ##build out query the code commented out was for original run in 2021 during Milestone 1
            # pytrend.build_payload([i],timeframe='2020-03-20 2021-11-24')
            pytrends.build_payload(kw_list=[i],timeframe='today 5-y')
            time.sleep(30)
            ##save trend to dictionary
            trends[i] = pytrends.related_queries()[i]

            # sleep to avoid 429 error 
            time.sleep(60)

        acnh_dict = dict()
        for item in acnh_villagers_two:
            i = trends[item]['rising']
            acnh_dict.update({item:i})
        
        print("good")
        return acnh_dict

    def convert_results(self, pytrend_dict):
        dict_list = []
        #dict_none = pd.DataFrame({"query":[np.nan],"value":[np.nan]})
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

    
start_acnh_pytrends = fetch_trends("/Users/jacquelineskunda/Documents/GitHub/699/SIADS_699_CAPSTONE/python_scripts_villagers/")
trend_payloads = start_acnh_pytrends.get_trends()
print(trend_payloads)
final_trends = start_acnh_pytrends.convert_results(trend_payloads)
