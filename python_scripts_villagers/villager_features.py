import pandas as pd 

class create_vil_feat():
    def __init__(self, path_file):
        self.path_file = path_file

    def astrology(self, day, mon):
        
        # using the day and month split on "-" to get the astrological sign of a villager
        if mon == 'Jan':
            if int(day) < 20:
                astro = 'Capricorn' 
            else: 
                astro = 'Aquarius'
            
        elif mon == 'Feb':
            astro = 'Aquarius' if int(day) < 19 else 'Pisces'
            
        elif mon == 'Mar':
            astro = 'Pisces' if int(day) < 21 else 'Aries'
            
        elif mon == 'Apr':
            astro = 'Aries' if int(day) < 20 else 'Taurus'
            
        elif mon== 'May':
            astro = 'Taurus' if int(day) < 21 else 'Gemini'
            
        elif mon == 'Jun':
            astro = 'Gemini' if int(day) < 21 else 'Cancer'
            
        elif mon == 'Jul':
            astro = 'Cancer' if int(day) < 23 else 'Leo'
            
        elif mon == 'Aug':
            astro = 'Leo' if int(day) < 23 else 'Virgo'
            
        elif mon == 'Sep':
            astro = 'Virgo' if (int(day) < 23) else 'Libra'
            
        elif mon == 'Oct':
            astro = 'Libra' if int(day) < 23 else 'Scorpio'

        elif mon == 'Nov':
            astro = 'Scorpio' if int(day) < 22 else 'Sagittarius'

        elif mon == 'Dec':
            astro = 'Sagittarius' if int(day) < 22 else 'Capricorn'
        else:
            astro = None
            
        return astro
    
    def villager_add_astro(self):
        
        # read in villager csv file with acp and py trends votes merged and convert birthday to usable field Astrology
        # for information retreival system
        villager_astro = pd.read_csv(self.path_file+"villagers_acnh_votes_combined.csv")
        
        # splitting the Birthday column on "-" and since split returns a list the first item aka zero index item is the day
        # and the second item aka index one item is the month
        villager_astro['Astrology'] = villager_astro['Birthday'].apply(lambda x: self.astrology(x.split("-")[0],x.split("-")[1])) # type: ignore
        villager_astro.to_csv(self.path_file+"villager_astro.csv")
        
        return villager_astro
    
    def music_genre(self, villager_w_astro, genre_file):

        # need to create a dictionary or csv mapping the song to the generalized music genre for quiz
        genre_list = villager_w_astro['Favorite Song'].tolist()
        
        # print(len(set(genre_list)))
        list_to_use = pd.DataFrame(set(genre_list),columns=['Favorite Song'])
        list_to_use.to_csv(self.path_file+"fav_song.csv")
       
        # now that we have researched and placed each unique song in its own genre we will attach
        # it to the df returned from the villager_add_astro def above
        genre_groups = pd.read_csv(genre_file)
        
        # merging the music with the villagers with astrology sign
        villagers_final = villager_w_astro.merge(genre_groups, how="left",on="Favorite Song")
        
        # removing columns from the df we will not need for the info retrieval sys and then
        # seperating the villager name and id along with filename to get the image in its own file 
        # creating the id and filename csv first
        villagers_id = villagers_final[['Name','Filename','Unique Entry ID']].copy()
        villagers_id.to_csv(self.path_file+"villagers_id.csv")

        # just in case creating a villagers_vote_rank.csv file to keep the votes/tallys sepearte from 
        # info retr. needed columns
        villagers_vote_rank = villagers_final[['Name','Unique Entry ID','Total_Google_Searches',
                                               'Poll_Results','Overall_Popularity']].copy()
        villagers_vote_rank.to_csv(self.path_file+"villagers_vote_rank.csv")

        #dropping the columns we will not need for the info retrieval system
        villagers_final.drop(columns = ['Catchphrase','Wallpaper','Flooring','Furniture List','Gender',
                                        'Filename','Unique Entry ID','Birthday','Favorite Song'],
                                         inplace = True)
        
        #reordering columns for ease of use when comparing user response order to quiz questions
        col_reorder = ['Name','Species','Personality','Hobby','Astrology','Genre',
                       'Style 1','Style 2','Color 1','Color 2',
                       'Total_Google_Searches','Poll_Results','Overall_Popularity']

        # creating the final csv for the info retrieval system
        villagers_final = villagers_final.reindex(columns=col_reorder)
        villagers_final.to_csv(self.path_file+"villagers_final.csv")

        


get_astro_genre_sign = create_vil_feat("./python_villagers_create/")
astro_added  = get_astro_genre_sign.villager_add_astro()
genre_added = get_astro_genre_sign.music_genre(astro_added,genre_file="./python_villagers_create/genre_groupings.csv")