import re
import os
import json

def add_all_general_ques(corpus_path,internal_dict): #this adds all the general conversational questions to our dictionary
    files=os.listdir(corpus_path)
    for n in files:
        file_path=corpus_path+'\\'+ n
        with open(file_path) as f:
            for p in question_pattern.findall(f.read()):
                internal_dict['intents'][0]['patterns'].append(p)
    return internal_dict
                
def to_json_file(yml_file,tag_pattern,question_pattern,answer_pattern,internal_dict,json_file):
#this segregates all the tags and their respective ques/ans ad add them to the given file
    with open(yml_file) as f:
        f.seek(0)
        matches=tag_pattern.finditer(f.read())
        for m in matches:
            internal_dict['intents'].append({'tag':m.group(1),'patterns':[],'responses':[]})

        f.seek(0)
        i=0
        for line in f:
            if re.match("categories:",line):
                i+=1
            else:
                if re.match(question_pattern,line):
                    internal_dict['intents'][i]['patterns'].append(re.match(question_pattern,line).group(1))
                else:
                    if re.match(answer_pattern,line):
                        internal_dict['intents'][i]['responses'].append(re.match(answer_pattern,line).group(1))             
    with open(json_file,'w') as f:
        f.write(json.dumps(internal_dict))
    print(f"Created and saved the trainable json file at:\n{os.path.abspath(json_file)}")
            
yml_file='yml_ques.yml' 
'''this is the yml file we have with all the questions we created through the yml creation script.
if you are in the same directory give the file name else the whole path'''
json_file='training_file.json' 
'''this is the json file we have to create for training the model
if you are in the same directory give the file name else the whole path 
(if you did not create any dummy file, don't worry justgive the name here it will be craeted autmatically)'''

tag_pattern=re.compile("categories:\n-\s(.*)") 
question_pattern=re.compile("-\s-\s(.*)")
answer_pattern=re.compile("\s{2}-\s(.*)")
#change these pattern if you have some different way of ques/ans and categories
internal_dict={'intents':
    [{'tag':'general',
      'patterns':[],
      'responses':[]}]
    }
#chabnge this style of dict if you have some other ays of training
corpus_path=r'C:\Users\Chinn\OneDrive\Desktop\FINALOVE\Projectandi\Training\corpus'
#this is the path where all the general conversational ques/ans reside as different files

internal_dict = add_all_general_ques(corpus_path,internal_dict)

to_json_file(yml_file,tag_pattern,question_pattern,answer_pattern,internal_dict,json_file)
