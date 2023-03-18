import pandas as pd
import numpy as np

class Connect_Res_Vill():
    def __init__(self, path_file_pytrend, path_file_acp_poll, path_out, villagers_file):
        self.path_file_pytrend = path_file_pytrend
        self.path_file_acp_poll = path_file_acp_poll
        self.path_out = path_out
        self.villagers_file = villagers_file

    def prep_fin_pytrend(self):
        # reading in pytrends_script.py resultant csv file to clean up and connect with villager.csv
        pytrend_res = pd.read_csv(self.path_file_pytrend)
        # prepareing the name to join/merge with villager.csv on Name and cleaning up some misled google query results
        pytrend_res['Name'] = pytrend_res['searchitem'].str.replace(r' Animal Crossing','')
        pytrend_res['Name2'] = pytrend_res['Name'].str.lower()
        pytrend_res['query'] = pytrend_res['query'].fillna('unknown')
        # baseline to keep query value is if the villager name is in the historical google query
        pytrend_res['keep_value'] = pytrend_res.apply(lambda x: x['Name2'] in x['query'], axis = 1)
        # now we fix misled google queries so we do not count there values in the final totals
        # fixing O'Hare name again
        pytrend_res['Name'] = np.where(pytrend_res['Name'] == 'OHare', "O'Hare", pytrend_res['Name'])
        # fixing June villager because June month results in query
        pytrend_res['keep_value'] = np.where(pytrend_res['Name'] == 'June', False, pytrend_res['keep_value'])
        # need to fix Lily the villager because all the searches done on her are actually for
        # the lily of the valley flower and its different colors and not for "her" as a villager.
        pytrend_res['keep_value'] = np.where(pytrend_res['Name'] == 'Lily', False, pytrend_res['keep_value'])
        # doing something similar for maple
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('maple leaf'),False,pytrend_res['keep_value'])
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('maple leaves'),False,pytrend_res['keep_value'])
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('maple diy'),False,pytrend_res['keep_value'])
        # doing a similar update for peaches because 'how to get peaches' refers to the fruit
        # and peachtree in the game not the villager
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('how to get peaches'),False,pytrend_res['keep_value'])
        # we will have to do the same for "cherry" the searches do not refer to the villager but the 
        # cherry blossoms and cherry tree and cherry salmon.
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('cherry blossom'),False,pytrend_res['keep_value'])
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('cherry tree'),False,pytrend_res['keep_value'])
        pytrend_res['keep_value'] = np.where(pytrend_res['query'].str.contains('cherry salmon'),False,pytrend_res['keep_value'])
        # now we can add up total value searches for each villager but first if keep value is False
        # we will update the search "value" to zero
        pytrend_res['value'] = np.where(pytrend_res['keep_value'] == False, 0,pytrend_res['value'])
    
        pytrend_search_count = pytrend_res.groupby(by=['Name'])[['value']].sum()
        pytrend_search_count = pytrend_search_count.reset_index()
        pytrend_search_count = pytrend_search_count.sort_values(by='value', ascending=False)
        # making sure there is 391 villagers
        print(pytrend_search_count.shape)

        #changing column name "value" to "Total_Google_Searches"
        pytrend_search_count = pytrend_search_count.rename(columns={"value": "Total_Google_Searches"})
        
        #Now we will merge this with the villagers acnh data
        villagers_acnh_google = pd.read_csv(self.villagers_file).merge(pytrend_search_count, left_on="Name",
                                            right_on = "Name", how = "left")

        return villagers_acnh_google

    def prep_fin_ACP(self,villagers_google):
        # reading in final ACP_Final.csv to process 
        ACP_POLL_FIN = pd.read_csv(self.path_file_acp_poll)

        # renaming columns for continuity with villagers.csv raw data file
        ACP_POLL_FIN = ACP_POLL_FIN.rename(columns = {'Tally':'Poll_Results',"Villagers":"Name"})

        # removing but Might need to delete this line of code at runtime
        ACP_POLL_FIN = ACP_POLL_FIN.drop("Unnamed: 0",axis=1)
        
        #merging to add on the poll results by villager name
        final_villagers_ACNH = villagers_google.merge(ACP_POLL_FIN, left_on="Name",
                                                  right_on='Name', how="left")
        #creating the total popularity villager value, may want to rate weight
        #and factorize the poll results value
        final_villagers_ACNH['Overall_Popularity'] = final_villagers_ACNH['Total_Google_Searches']+final_villagers_ACNH['Poll_Results']
        
        #checking number of rows for correctness and number of proper villagers
        print(final_villagers_ACNH.shape)
        
        return final_villagers_ACNH.to_csv(self.path_out+'villagers_acnh_votes_combined.csv')
    

start_connect = Connect_Res_Vill(path_file_pytrend ="./python_scripts_villagers/final_pytrends.csv",
                                 path_file_acp_poll = "./python_scripts_villagers/ACP_Final.csv", 
                                 path_out = "./python_scripts_villagers/", 
                                 villagers_file= "./python_scripts_villagers/villagers.csv")
vil_w_pytrend = start_connect.prep_fin_pytrend()
vil_w_acp_pytrend = start_connect.prep_fin_ACP(vil_w_pytrend)
    
