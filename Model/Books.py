import spacy
import itertools
import pandas as pd
from functools import reduce

class Books_Data:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_sm')
        file=pd.ExcelFile('ProcessedLib.xlsx')
        sheets=file.sheet_names
        self.books_df=pd.read_excel(file,sheet_name=sheets[0])
        for sheet in sheets[1:]:
            self.books_df=pd.concat([self.books_df,pd.read_excel(file,sheet_name=sheet)])
        self.rem_words=['and','how','what','many','books','available','copies','where','is','are','the','in','of','there','here','all','for','do','you','know']
    def get_books_data(self,converse,input_columns,output_columns):
        temp=list(map(lambda input_column:self.books_df[input_column].values.tolist(),input_columns))
        books=temp[0]
        if(len(books)>1):
            for _ in temp[1:]:
                books.extend(_)
        text=self.nlp(converse)
        results=list()
        for entity in text.ents:
            book_match=list()
            for i,book in enumerate(books):
                if(type(book) is str):
                    if(entity.text.lower() in book.lower()):
                        book_match.append(book)
            if(len(book_match)>0):
                results.append(book_match)
        if(len(text.ents)==0):
            for word in text:
                if(word.text.lower() not in self.rem_words and (not word.is_stop)):
                    print(word)
                    book_match=list()
                    for i,book in enumerate(books):
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
            for i,r in enumerate(map(lambda x:self.books_df.iloc[books.index(x)],res_mat)):
                output.append(r[output_columns])
        return output
    def library(self,converse,tag):
        if(tag=='books_name'):
            books_by_name=self.get_books_data(converse,['BookName'],self.books_df.columns)
            if(len(books_by_name)==0):
                books_by_name=None
            if(books_by_name is None):
                return 'Sorry! no book available with that name'
            return pd.DataFrame(books_by_name)
        elif(tag=='books_author'):
            books_by_author=self.get_books_data(converse,['AuthorName'],self.books_df.columns)
            if(len(books_by_author)==0):
                books_by_author=None
            if(books_by_author is None):
                return 'Sorry! no books of that author'
            return pd.DataFrame(books_by_author)
        elif(tag=='books_number'):
            output='Number of copies of each book:<br/>'
            books_by_author=self.get_books_data(converse,['AuthorName'],['AuthorName','CopiesNumber'])
            books_by_name=self.get_books_data(converse,['BookName'],['BookName','CopiesNumber'])
            if(len(books_by_author)==0):
                books_by_author=None
            if(len(books_by_name)==0):
                books_by_name=None
            if(books_by_name is None):
                if(books_by_author is None):
                    return 'Sorry! no book available'
                else:
                    output+='Author Name : Number of copies <br/>'
                    for x in books_by_name:
                        output+=x['AuthorName']+':'+str(x['CopiesNumber'])+'<br/>'
                    return output
            elif(books_by_author is None):
                output+='Book Name : Number of copies<br/>'
                for x in books_by_name:
                    output+=x['BookName']+':'+str(int(x['CopiesNumber']))+'<br/>'
                return output
            else:
                output+='Book Name : Number of copies<br/>'
                for x in books_by_name:
                    output+=x['BookName']+':'+str(int(x['CopiesNumber']))+'<br/>'
                output+='Author Name : Number of copies<br/>'
                for x in books_by_author:
                    output+=x['AuthorName']+':'+str(x['CopiesNumber'])+'<br/>'
                return output