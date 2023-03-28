from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import requests
from io import BytesIO


class RetrievalSystem(object):
    def __init__(self, path_file,num_topics =-1, 
                 min_df=1, user_list = [],
                 ):
        """
        RetrievalSystem setup for lsi, creation of doc term matrix, and query vectors
        """
        self.path_file = path_file
        self.villagers = pd.read_csv(self.path_file+"villagers_final.csv")
        self.user_list = user_list
        self.villagers_id= pd.read_csv(self.path_file+"villagers_id.csv")
        
        self.villagers.drop(columns=['Unnamed: 0'],inplace=True)
        
        villagers_lines = self.villagers[['Species','Personality','Hobby','Astrology','Genre','Style 1','Style 2','Color 1','Color 2']].copy()
        villagers_lines = villagers_lines.apply(lambda x: x.astype(str).str.lower())
        villagers_arr = villagers_lines.to_numpy()
        
        # create a doc-term matrix out of our doc collection
        self.vec = TfidfVectorizer(tokenizer=str.split, min_df=min_df)
        doc_term_mat = self.vec.fit_transform([" ".join(vil) for vil in villagers_arr])
        
        #lsi
        self.lsi = TruncatedSVD(n_components=num_topics,random_state=42,algorithm='randomized')
        
        # Fit SVD model on data
        self.doc_vecs = self.lsi.fit_transform(doc_term_mat) # document vectors in a matrix
        
        #create query vectors
        self.q_vecs = dict()
       
        
    def retrieve_n_rank_docs(self):
        """
        Retrieve and rank documents in the latent semantic (concept) space
        """
        
        def getcossim(q_vec,docdict):
            
            cos_val = cosine_similarity(q_vec.reshape(1, -1) , docdict.reshape(1, -1))
            
            if np.isnan(cos_val):
                return cos_val == 0
            else:
                return cos_val[0]
        
        #create doc vectors
        d_vecs = dict()
        for i,vec in enumerate(self.doc_vecs):
            d_vecs[i]=vec

        # create cosim values per villager based on user list   
        cos_ret_docs=dict()
        for i,q in d_vecs.items():
            new_q_uid_vec = self.vec.transform([" ".join(self.user_list)])
            q_id_vec_user = self.lsi.transform(new_q_uid_vec)
            cossim = getcossim(q_id_vec_user, q)
            cos_ret_docs[i] = cossim
        
        # sort the cosim values and return the top 2 villagers
        ret_docs_1 = dict(sorted(cos_ret_docs.items(), key = lambda x: x[1], reverse=True))
        ret_docs_df = pd.DataFrame.from_dict(ret_docs_1,orient="index",columns=['cosine_similarity'])
        ret_docs_df['cosine_similarity'] = ret_docs_df['cosine_similarity'].apply(lambda x: round(x,2))
        ret_docs_df = ret_docs_df.merge(self.villagers,how='left',left_index=True,right_index=True)
        ret_docs_df['tup_col'] = list(zip(ret_docs_df.cosine_similarity, ret_docs_df.Overall_Popularity))
        ret_docs_dict = dict(zip(ret_docs_df.Name, ret_docs_df.tup_col))
        ret_docs = dict(sorted(ret_docs_dict.items(), key = lambda x: (x[1],x[0]), reverse=True))
        
        vil_1 = list(ret_docs.keys())[0]
        vil_2 = list(ret_docs.keys())[1]

        return vil_1, vil_2

    def get_villagers_id(self, vil_1, vil_2):
        """ 
        Retrieve the villagers id from the villagers_id dataframe to use to bring back images for the webpage
        results.
        """
        vil_1_id =self.villagers_id[self.villagers_id['Name'] == vil_1]['Filename'].item()
        vil_2_id = self.villagers_id[self.villagers_id['Name'] == vil_2]['Filename'].item()
        vil_1_tup = (vil_1,vil_1_id)
        vil_2_tup = (vil_2,vil_2_id)
        
        return vil_1_tup, vil_2_tup
    
    def return_image(self, vil_1_tup, vil_2_tup):
        """
        Retrieve the villagers image from the api and return the image to the webpage.
        """
        v_name1 = vil_1_tup[0]
        v_name2 = vil_2_tup[0]

        url_vil1 = f'https://acnhapi.com/v1a/images/villagers/{vil_1_tup[1]}'
        response_vil1 = requests.get(url_vil1)
        img_vil1 = Image.open(BytesIO(response_vil1.content))
        # img_vil1.show(title = str(v_name1))

        url_vil2 = f'https://acnhapi.com/v1a/images/villagers/{vil_2_tup[1]}'
        response_vil2 = requests.get(url_vil2)
        img_vil2 = Image.open(BytesIO(response_vil2.content))
        # img_vil2.show(title = str(v_name2))

        return v_name1, img_vil1.show(title = str(v_name1)), v_name2, img_vil2.show(title = str(v_name2))
    
if __name__ == "__main__":
    user_sim_cl = RetrievalSystem(path_file = ("./python_scripts_villagers/"), num_topics=9,
                              user_list = ['Cub','Cranky','Play','Taurus','Funk','Simple','Active','Green','Light blue'],
                              )
    villager_1, villager_2 = user_sim_cl.retrieve_n_rank_docs()
    v_id1, v_id2 = user_sim_cl.get_villagers_id(vil_1 = villager_1, vil_2 = villager_2)
    v_name1, v_img1, v_name2, v_img2 = user_sim_cl.return_image(v_id1, v_id2)
    # print(v_id1, v_id2)
    