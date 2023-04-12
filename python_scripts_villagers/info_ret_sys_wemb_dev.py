import spacy
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import en_core_web_sm
# importing modules for image retrieval
from PIL import Image
import requests
from io import BytesIO

class RetrievalSystem_wb:
    def __init__(self, path_file,user_list = []):
        """
        RetrievalSystem setup for spacy word embeddings,creation of doc vectors and user vector 
        """
        self.path_file = path_file
        self.villagers = pd.read_csv(self.path_file+"villagers_final.csv")
        self.user_list = user_list
        self.villagers_id= pd.read_csv(self.path_file+"villagers_id.csv")
        self.villagers_rank= pd.read_csv(self.path_file+"villagers_vote_rank.csv")
        self.villagers.drop(columns=['Unnamed: 0'],inplace=True)
        
        villagers_lines = self.villagers[['Species','Personality','Hobby',
                                          'Astrology','Genre','Style 1','Style 2','Color 1','Color 2']].copy()
        
        villagers_lines.loc[len(villagers_lines)] = user_list # type: ignore
        
        villagers_lines = villagers_lines.apply(lambda x: x.astype(str).str.lower())
        self.villagers_arr = villagers_lines.to_numpy()
        
        
        self.nlp = en_core_web_sm.load()
        self.doc = [self.nlp(" ".join(villager_line)) for villager_line in self.villagers_arr]
        self.user = self.doc[-1].vector
        self.doc_vil = self.doc[:-1]
    

    def get_cossim_villagers(self):
        """
        Calculate the cosine similarity between the user vector and the villagers vector
        """
        
        similarity_vil = []
        for i in range(len(self.doc_vil)):
            row = cosine_similarity(self.user.reshape(1, -1), self.doc_vil[i].vector.reshape(1,-1))[0][0] # type: ignore
            similarity_vil.append(round(row,2))
        
        return similarity_vil
    
    def finalize_sim_villagers(self, similarity_vil):
        """ 
        Fetch the top 2 villagers based on similarity score and return the name and ID of the villagers.
        """

        self.villagers['Similarity'] = similarity_vil
        self.villagers['Similarity'] = self.villagers['Similarity'].astype(float)
        self.villagers['ID'] = self.villagers_id['Filename'].tolist()
        villagers_sorted = self.villagers.copy()
        villagers_sorted = villagers_sorted.sort_values(by=['Similarity','Overall_Popularity'],
                                                   ascending=[False,False]).reset_index()
        
        vil_1_id = villagers_sorted.loc[0,'ID']
        vil_1 = villagers_sorted.loc[0,'Name']
        vil_2_id = villagers_sorted.loc[1,'ID']
        vil_2 = villagers_sorted.loc[1,'Name']

        vil_1_tup = (vil_1,vil_1_id)
        vil_2_tup = (vil_2,vil_2_id)
        return vil_1_tup, vil_2_tup
    
    def return_image(self, vil_1_tup, vil_2_tup):
        """Retrieve image of villagers from API and return image and name of villagers"""

        v_name1 = vil_1_tup[0]
        v_name2 = vil_2_tup[0]

        url_vil1 = f'https://acnhapi.com/v1a/images/villagers/{vil_1_tup[1]}'
        response_vil1 = requests.get(url_vil1)
        img_vil1 = Image.open(BytesIO(response_vil1.content))
        
        url_vil2 = f'https://acnhapi.com/v1a/images/villagers/{vil_2_tup[1]}'
        response_vil2 = requests.get(url_vil2)
        img_vil2 = Image.open(BytesIO(response_vil2.content))
        

        return v_name1, img_vil1.show(title = str(v_name1)), v_name2, img_vil2.show(title = str(v_name2))

if __name__ == "__main__":
    user_sim_cls = RetrievalSystem_wb(path_file = ("./python_scripts_villagers/"),
                                user_list = ['Cat','Smug','Fitness','Gemini','Electronic','Active','Gorgeous','Green','Light Blue'],
                                )
    villager_sim = user_sim_cls.get_cossim_villagers()
    v_id1, v_id2 = user_sim_cls.finalize_sim_villagers(villager_sim)
    
    v_name1, v_img1, v_name2, v_img2 = user_sim_cls.return_image(v_id1, v_id2)