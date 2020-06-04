import re
import spacy
import itertools
import pandas as pd
from functools import reduce

class search_direct:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_sm')
        file=pd.ExcelFile('ProcessedLib.xlsx')
        sheets=file.sheet_names
        self.books_df=pd.read_excel(file,sheet_name=sheets[0])
        for sheet in sheets[1:]:
            self.books_df=pd.concat([self.books_df,pd.read_excel(file,sheet_name=sheet)])
        self.books=self.df_to_list(['BookName'])
        self.authors=self.df_to_list(['AuthorName'])
    def df_to_list(self,input_columns):
        temp=list(map(lambda input_column:self.books_df[input_column].values.tolist(),input_columns))
        lists=temp[0]
        if(len(lists)>1):
            for _ in temp[1:]:
                lists.extend(_)
        return lists
    def get_results(self,converse,data_list):
        text=self.nlp(converse.lower())
        results=list()
        for word in text:
            #print(word)
            book_match=list()
            for i,book in enumerate(data_list):
                if(type(book) is str):    
                    if(word.text.lower() in book.lower()):
                        book_match.append(book)
            if(len(book_match)>0):
                results.append(set(book_match))
        #print(results)
        comb_results=list(map(lambda i:list(itertools.combinations(range(len(results)),i)),range(1,len(results)+1)))
        #print(comb_results)
        res_match=list()
        for comb_result in comb_results[-1::-1]:
            res_match=list()
            for tuples in comb_result:
                if(tuples[0]==tuples[-1]):
                    temp3=list(set(results[0]))
                    if(temp3 not in res_match):
                        res_match.append(temp3)
                else:
                    res_match.append(list(reduce(lambda i, j: i & j, (set(x) for x in results[tuples[0]:tuples[-1]+1]))))
            if(len(res_match)!=0 and not (len(res_match)==1 and len(res_match[0])==0)):
                break
        #print(res_match)
        output=list()
        for res_mat in res_match:
            for i,r in enumerate(map(lambda x:self.books_df.iloc[data_list.index(x)],res_mat)):
                output.append(r)
            output_df=pd.DataFrame(output)
            #print(output_df)
        return output_df
    def search(self,books_by_name,books_by_author):
        result_by_name=pd.DataFrame(columns=self.books_df.columns)
        result_by_author=pd.DataFrame(columns=self.books_df.columns)
        if(books_by_name is not None):
            none_flag=False
            if(len(books_by_name)>0):
                result_by_name=self.get_results(books_by_name,self.books)
            else:
                none_flag=True
        if(books_by_author is not None):
            if(len(books_by_author)>0):
                result_by_author=self.get_results(books_by_author,self.authors)
                none_flag=False
        if(none_flag):
            return 'Tell me better! (No record found)'
        elif(len(books_by_name)==0):
            return 'Here you go! \n{}'.format(result_by_author)
        elif(len(books_by_author)==0):
            return 'Here you go! \n{}'.format(result_by_name)
        combined=pd.merge(result_by_author,result_by_name, how='inner', on=['BookName'])
        if(len(combined)==0):
            return "This author has no book with that name, but we found some books of the author and the name seperately \n Author:\n {}\n Name: \n {}".format(result_by_author,result_by_name)
        else:
            return "Here you go! \n{}".format(combined.iloc[:,:len(self.books_df.columns)])
if __name__=='__main__':
    sd=search_direct()
    print(sd.search('analog integrated circuits','Sergio'))