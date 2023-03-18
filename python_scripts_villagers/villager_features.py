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
        villager_astro.to_csv(self.path_file+"villager_fin_astro.csv")
        return villager_astro
    
    def music_genre(self, villager_w_astro):
        # need to create a dictionary or csv mapping the song to the generalized music genre for quiz
        pass


get_astro_sign = create_vil_feat("./python_scripts_villagers/")
astro_added  = get_astro_sign.villager_add_astro()