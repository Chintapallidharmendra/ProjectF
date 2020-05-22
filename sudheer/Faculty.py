import spacy
import pandas as pd

class Faculty_Data:
    def __init__(self):
        self.nlp=spacy.load('en_core_web_sm')
        self.faculty_df=pd.read_excel('faculties.xlsx')
    def get_faculty_data(self,converse,input_columns,output_columns):
        fac=self.faculty_df[input_columns]
        fac=fac.values.tolist()
        text=self.nlp(converse)
        for x in text.ents:
            #print(type(x),x)
            for i,y in enumerate(fac):
                if x.text.lower() in y[0].lower() or x.text.lower() in y[1].lower():
                    return self.faculty_df.loc[i,output_columns]
        for x in text:
            if(not x.is_stop and x is not None):
                for i,y in enumerate(fac):
                    if x.text.lower() in y[0].lower() or x.text.lower() in y[1].lower():
                        return self.faculty_df.loc[i,output_columns]     
    def faculty(self,converse,tag):
        #print(tag)
        if(tag=='faculty_timings'):
            if('Available'.lower() in converse.lower()):
                availability=self.get_faculty_data(converse,['Faculty','Code'],['Available'])[0]
                if(availability=='yes'):
                    return 'Avaliable'
                else:
                    return 'Unavailable'
            else:
                timings=self.get_faculty_data(converse,['Faculty','Code'],['Time in', 'Time out'])
                if(timings is None):
                    return 'Sorry! no faculty with that name'
                return 'Time in: {}, Time out: {}'.format(timings[0],timings[1])
        elif(tag=='faculty_location'):
            location=self.get_faculty_data(converse,['Faculty','Code'],['Floor'])
            if(location is None):
                return 'Sorry! no faculty with that name'
            return '{} Floor'.format(location[0])
        elif(tag=='faculty_teachings'):
            teachings=self.get_faculty_data(converse,['Faculty','Code'],['Teaching','Teaching_Code','Faculty'])
            subjects=self.get_faculty_data(converse,['Teaching','Teaching_Code'],['Faculty','Code'])
            #print(teachings,subjects)
            if(teachings is None and subjects is None):
                return "Sorry! no faculty with that name"
            elif(teachings is None):
                return '{}({})'.format(subjects[0],subjects[1])
            elif(subjects is None):
                return '{}({})'.format(teachings[0],teachings[1])
            else:
                if(teachings[2]==subjects[0]):
                    return 'yes'
                else:
                    return 'no'
        else:
            return 'Tell  me more!'