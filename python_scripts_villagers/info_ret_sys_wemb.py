import spacy
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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
        villagers_lines = villagers_lines.apply(lambda x: x.astype(str).str.lower())
        villagers_lines.loc[len(villagers_lines)] = user_list
        
        self.villagers_arr = villagers_lines.to_numpy()
        
        
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = [self.nlp(" ".join(villager_line)) for villager_line in self.villagers_arr]
        self.user = self.doc[-1].vector
        self.doc_vil = self.doc[:-1]
        print(self.doc[-1].vector)
    

    def get_cossim_villagers(self):
        similarity_vil = []
        for i in range(len(self.doc_vil)):
            row = cosine_similarity(self.user.reshape(1, -1),self.doc_vil[i].vector.reshape(1, -1))[0][0]
            similarity_vil.append(round(row,2))
        
        return similarity_vil
    
    def finalize_sim_villagers(self, similarity_vil):
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
    

if __name__ == "__main__":
    user_sim_cls = RetrievalSystem_wb(path_file = ("./SIADS_699_CAPSTONE/python_scripts_villagers/"),
                                user_list = ['Frog','Big Sister','Fitness','Gemini','Electronic','Active','Gorgeous','Green','Light Blue'],
                                )
    villager_sim = user_sim_cls.get_cossim_villagers()
    print(sorted(villager_sim,reverse=True)[0:11])
    v_id1, v_id2 = user_sim_cls.finalize_sim_villagers(villager_sim)
    print(v_id1, v_id2)

v_name1 = v_id1[0]
v_name2 = v_id2[0]

# importing modules
from PIL import Image
import requests
from io import BytesIO

url = f'https://acnhapi.com/v1a/images/villagers/{v_id1[1]}'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show(title = str(v_name1))