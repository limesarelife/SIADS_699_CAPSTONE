import pandas as pd
import os

"""There are different file formats in the 2020 files so I am going to read each one in by itself 
with for loop and just pull the Villagers and Tally columns since that is all we need and then 
combine the 2021 and 2020 data sets into one total dataframe to link to the Villagers.csv and 
attach the ACP_Poll_Votes aka "Tally". We might need to clean some names."""
class ACP_Combine:
    def __init__(self, path_file):
        self.path_file = path_file
    def get2020ACP(self):

        ACP_PollRes2020 = pd.DataFrame()
        for root, dirs, files in os.walk(self.path_file):
            for file in files:
                filename = file
                print(filename)
                if '2020' in filename:
                    df = pd.read_excel(self.path_file+filename)
                    df = df[['Villagers','Tally']]
                    #df = df[df['Villagers']].notna()
                    ACP_PollRes2020 = ACP_PollRes2020.append(df) # type: ignore
        # Removing villagers who never received any votes
        ACP_PollRes2020 = ACP_PollRes2020[ACP_PollRes2020['Villagers'].notna()].copy()

        # Getting full tally of votes for Villagers with groupby
        ACP_2020 = ACP_PollRes2020.groupby(by = 'Villagers',dropna=True).Tally.sum().reset_index()
        # Sorting in asecending order
        ACP_2020 = ACP_2020.sort_values(['Tally'], ascending = False)
        # Resetting index
        ACP_2020 = ACP_2020.reset_index(drop = True).copy()

        return ACP_2020

    # Repeating similar process for 2021 ACP Polls
    def get2021ACP(self):

        ACP_PollRes2021 = pd.DataFrame()
        for root, dirs, files in os.walk(self.path_file):
            for file in files:
                filename = file
                print(filename)
                if '2021' in filename:
                    df = pd.read_excel(self.path_file+filename)
                    df = df[['Villagers','Tally']]
                    #df = df[df['Villagers']].notna()
                    ACP_PollRes2021 = ACP_PollRes2021.append(df) # type: ignore
        
        # Getting full tally of votes for Villagers with groupby
        ACP_2021 = ACP_PollRes2021.groupby(by = 'Villagers',dropna=True).Tally.sum().reset_index()
        # Sorting in asecending order
        ACP_2021 = ACP_2021.sort_values(['Tally'], ascending = False)
        # Resetting index
        ACP_2021 = ACP_2021.reset_index(drop = True)

        return ACP_2021
    
    def get2022ACP(self):

        ACP_PollRes2022 = pd.DataFrame()
        for root, dirs, files in os.walk(self.path_file):
            for file in files:
                filename = file
                print(filename)
                if '2022' in filename:
                    df = pd.read_excel(self.path_file+filename)
                    df = df[['Villagers','Tally']]
                    #df = df[df['Villagers']].notna()
                    ACP_PollRes2022 = ACP_PollRes2022.append(df) # type: ignore
        
        # Getting full tally of votes for Villagers with groupby
        ACP_2022 = ACP_PollRes2022.groupby(by = 'Villagers',dropna=True).Tally.sum().reset_index()
        # Sorting in asecending order
        ACP_2022 = ACP_2022.sort_values(['Tally'], ascending = False)
        # Resetting index
        ACP_2022 = ACP_2022.reset_index(drop = True)

        return ACP_2022

    # Concat of two ACP polls into one df
    def combine_clean_ACP(self,f1,f2,f3,path_out):
        ACP_FinalDF = pd.concat([f1, f2, f3], axis=0)

        # Repeating the same groupby process about to the get the total 
        # tally sum of voted from Animal Crossing Portal by villager
        ACP_FinalDF = ACP_FinalDF.groupby(by = 'Villagers',dropna=True).Tally.sum().reset_index()
        ACP_FinalDF = ACP_FinalDF.sort_values(['Tally'], ascending = False)
        ACP_FinalDF = ACP_FinalDF.reset_index(drop = True)

        """We have some name variations of the same villagers, we will have to clean those a bit.
        Goal is to check the villager names but will have to convert to list 
        and then sort ascending and look at the names independently."""
        
        #  chknames = sorted(ACP_FinalDF.Villagers.to_list())

        """Context, feel free to print out chknames above - we had to research if these were dupes
        with spelling variations and change accordingly
        Need to check Annalise and Annalisa (edit: checked anteater and horse so okay), 
        Curlos and Curly(edit: sheep and pig), 
        Del and Deli(edit: alligator and monkey), 
        Remove Nan (edit: is a goat), 
        Tammi and Tammy (edit: monkey and cub(bear)), 
        Ursula and Ursala (edit: need to change Ursula to Ursala, 
        just one character/villager that is a cub(bear)). 
        (Note: Possibly switch O'Hare to OHare and fix 
        Renee with tilde for joining purposes)"""

        #fixing Ursula to Ursala
        ACP_FinalDF["Villagers"].replace({"Ursula": "Ursala"}, inplace=True)
        #redoing groupbyto fix Ursala totals
        ACP_FinalDF = ACP_FinalDF.groupby(by = 'Villagers',dropna=True).Tally.sum().reset_index()
        ACP_FinalDF = ACP_FinalDF.sort_values(['Tally'], ascending = False)
        ACP_FinalDF = ACP_FinalDF.reset_index(drop = True)

        """ In milestone 1 we needed to check why 'Chai','Chelsea', 'Marty', 'Rilla', 'Toby','Étoile' are 
            not in villagers.csv file. Are they brand new? Upon further research these villagers: 
            Chai, Chelsea, Marty, Rilla, Toby and Etoile are from the Sanrio update so they will 
            not be in our Villagers datset. 
            When joining the two data sets villagers.csv and the ACP_FinalDF they will disappear :)"""
        
        return ACP_FinalDF.to_csv(path_out+"ACP_Final.csv")
    
start_acp = ACP_Combine("./ACP_POLLS/")
acp2020 = start_acp.get2020ACP()
acp2021 = start_acp.get2021ACP()
acp2022 = start_acp.get2022ACP()
final_acp = start_acp.combine_clean_ACP(acp2020,acp2021,acp2022,path_out="../SIADS_699_CAPSTONE/python_villagers_create/")

