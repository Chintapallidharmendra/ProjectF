import spacy
import pandas as pd
class search_direct:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_sm')
        self.faculty_df=pd.read_excel('faculties.xlsx')
        self.faculties=self.faculty_df['Faculty'].values.tolist()
    def search(self,converse):
        text=self.nlp(converse.lower())
        for x in text:
            for i,y in enumerate(self.faculties):
                if x.text.lower() in y.lower():
                    return self.faculty_df.loc[i,:]
if __name__=='__main__':
    sd=search_direct()
    print(sd.search('darji').to_frame(name='Resutls'))