import xlrd

def read_data(file_path):
    """reads data from a file and returns it"""
    file_path = r"{}".format(file_path)
    with open(file_path, "r") as file:
        data = file.readlines()
    return data

def write_data(file_path, data):
    """writes data to a file"""
    file_path = r"{}".format(file_path)
    with open(file_path, "w") as file:
        for line in data:
            file.write(line)

def add_category(file_path, category):
    """adds a category to the yml file given"""
    file_path = r"{}".format(file_path)
    with open(file_path, "a") as file:
        file.write("\ncategories:\n- {}\n".format(category))
        file.write("conversations:\n")
    
def isList(var):
    return type(var) == type([])

def fetch_index(file_path, data, category):
    try:
        req_index = data.index("- " + category + "\n") + 2
    except ValueError:
        add_category(file_path, category)
        data = read_data(file_path)
        req_index = data.index("- " + category + "\n") + 2
    return req_index, data

def extract_qna(file_path, category):
    """prepares common questions and answers in the given category from the yml file given for training"""
    data = read_data(file_path)
    questions = []
    answers = []
    start_index = data.index("- " + category + "\n") + 2
    end_index = -1
    for i in range(start_index, len(data)-1):
        if "categories:" in data[i]:
            end_index = i
            break 
        if "- - " in data[i]:
            questions.append(data[i])
            answers.append(data[i+1])
    return questions, answers, end_index, data

def add_specific_ques(file_path, questions, answers, names, category):
    """adds a question to the file specified. question is expected to be in a specific format"""
    file_path = r"{}".format(file_path)
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    data = read_data(file_path)
    req_index, data = fetch_index(file_path, data, category)
    for i in range(len(questions)):
        final_qstns = [questions[i].replace("_", name) for name in names]
        for j in range(len(final_qstns)):
            data.insert(req_index, "\n- - {}\n  - {}\n".format(final_qstns[j], answers[j%(len(answers))])) # a reasonable assumption made here is that there would not be more answers than the questions
    write_data(file_path, data)
    ques, ans, end_index, data = extract_qna(file_path, category)
    ques = list(dict.fromkeys(ques))
    ans = ans[:len(ques)]
    if not (len(ques) == 0 | len(ans) == 0):
        qna_list = ['\n{}{}'.format(ques[i], ans[i]) for i in range(len(ques))]
        if end_index != -1:
            data = data[:req_index] + qna_list + data[end_index:]
        else:
            data = data[:req_index] + qna_list
    write_data(file_path, data)
    
def add_general_ques(file_path, questions, answers, category):
    """adds a general type question to the file specified"""
    file_path = r"{}".format(file_path)
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    data = read_data(file_path)
    req_index, data = fetch_index(file_path, data, category)
    for i in range(len(questions)):
        data.insert(req_index, "\n- - {}\n  - {}\n".format(questions[i], answers[i%(len(answers))]))
    write_data(file_path, data)
    ques, ans, end_index, data = extract_qna(file_path, category)
    ques = list(dict.fromkeys(ques))
    ans = ans[:len(ques)]
    if not (len(ques) == 0 | len(ans) == 0):
        qna_list = ['\n{}{}'.format(ques[i], ans[i]) for i in range(len(ques))]
        if end_index != -1:
            data = data[:req_index] + qna_list + data[end_index:]
        else:
            data = data[:req_index] + qna_list
    write_data(file_path, data)

def add_book_by_author_ques(file_path, questions, answers, book_names, author_names, category):
    """another project specific function to add a specific type of question to the given yml file"""
    file_path = r"{}".format(file_path)
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    data = read_data(file_path)
    req_index, data = fetch_index(file_path, data, category)
    for i in range(len(questions)):
        qstns_temp = []
        final_qstns = []
        ind = questions[i].index("_")
        qstns_temp.extend([(questions[i][:ind] + book_name + questions[i][ind+1:]) for book_name in book_names])
        for question in qstns_temp:
            ind = question.index("_")
            final_qstns.extend([(question[:ind] + author_name + question[ind+1:]) for author_name in author_names])
        for j in range(len(final_qstns)):
            data.insert(req_index, "\n- - {}\n  - {}\n".format(final_qstns[j], answers[j%(len(answers))]))
    write_data(file_path, data)
    ques, ans, end_index, data = extract_qna(file_path, category)
    ques = list(dict.fromkeys(ques))
    ans = ans[:len(ques)]
    if not (len(ques) == 0 | len(ans) == 0):
        qna_list = ['\n{}{}'.format(ques[i], ans[i]) for i in range(len(ques))]
        if end_index != -1:
            data = data[:req_index] + qna_list + data[end_index:]
        else:
            data = data[:req_index] + qna_list
    write_data(file_path, data)
    
def read_excel(file_path):
    """reads an excel file (with one sheet) and returns the data"""
    file_path = r"{}".format(file_path)
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(0)
    col_names = []
    data = {}
    for i in range(sheet.ncols):
        col_names.append(sheet.cell_value(0, i))
    for col in col_names:
        data[col] = []
    for i in range(sheet.ncols):
        col = col_names[i]
        for j in range(1, sheet.nrows):
            data[col].append(sheet.cell_value(j, i))
    return data

def read_excel_mult_sheets(file_path):
    """project specific function to read data from multiple sheets of an excel file"""
    file_path = r"{}".format(file_path)
    wb = xlrd.open_workbook(file_path)
    sheet_names = wb.sheet_names()
    col_names = []
    data = {}
    col_indices = [1,2] #column indices in each sheet to be fetched
    col_names = ["book_name", "author_name"]
    for col_name in col_names:
        data[col_name] = [] # we do this since all the sheets have the same type of data in the corresponding columns. Hence appending data across the sheets wont have any negative effect
    for ind in range(len(sheet_names)):
        sheet = wb.sheet_by_index(ind)
        for i in range(2):
            for j in range(sheet.nrows):
                data[col_names[i]].append(sheet.cell_value(j, col_indices[i]))
    for col_name in col_names:
        data[col_name] = [ele for ele in data[col_name] if ele != ''] #remove empty entries, cant be used for conversation 
        data[col_name] = list(set(data[col_name])) #remove duplicate elements, showing all entries related to this element would be better
    data["subjects"] = sheet_names
    return data


if __name__ == "__main__":
    print("Provide the relative file path from cwd or give the absolute path")
    excel_file_path = input("Excel file path (for the faculty information) : ")
    yml_file_path = input("YML file path : ")
    excel_lib_file_path = input("Excel file path (for the library database) : ")
    excel_dict = read_excel(excel_file_path)
    excel_lib_dict = read_excel_mult_sheets(excel_lib_file_path)
    faculty_names = excel_dict["Faculty"]
    book_names = excel_lib_dict["book_name"]
    author_names = excel_lib_dict["author_name"]
    subjects = excel_lib_dict["subjects"]
    faculty_code_names = excel_dict["Code"]

    faculty_names.extend(faculty_code_names)

    book_name_questions = ["is _ available in the library?","Is the book _ there?","Any book named _?", "Can you search for the availability of _?"]
    book_author_questions = ["What all are the books written by _?", "Books written by _?", "Books of _?","Which of _'s books are available?",
                             "Can I get any of _'s books?", "Can you search for the availability of book written by _?"]
    book_number_questions = ["How many books named _ are avaiable?","How many copies of _ are there?", "Can I know how many copies of _ are there?",
                             "Number of books of _?", "Books number of _"]
    book_number_answers = ["As per the inventory, there are: ","Let me peek through... There are: ","The number books available are:", "Yes, the number is: ",
                           "There must be around: "]
    book_by_author_questions = ["is _ by _ available?"]
    
    faculty_location_q = ["is _ in the office?", "Where does _ sit?", "Where is _ cabin?","Where does _ reside in the department?"]
    faculty_location_a = ["let me check the database for that: ", "I have to check their time table for that. Please wait: ", "Kindly wait while I check the database: "]
    faculty_teachings_q = ["Which subject does _ teach?", "Which classes does _ take?","Does _ teach DCN?", "Subjects taught by _",
                         "What are _'s specializations?","What are the specializations of _?"]
    faculty_teachings_a = ["Accessing faculty database: ", "The details you need are as follows : ", "Here are the requested details: "]
    faculty_timings_q = ["When is _ available?", "Timings of _'s availability", "Till when is _ in department?", "When can I meet _?"]
    faculty_timings_a = ["Here are your details, please note that these might be incorrect: ", "Requested timing details are as follows : "]
    faculty_HOD_q = ["Who is the HOD?", "Who is the Head of the Department?", "Where is the HOD's cabin?"]
    faculty_HOD_a = ["As per the database, the current HOD's details are: ", "Current HOD details are (these might be incorrect): "]
    faculty_general_q = ["Who are the professors in the department?", "Who are the asst. professors in the department?", "Who are the teaching assistants in the department?"]
    faculty_general_a = ["List of the faculty in the department: ", "Presenting all the information related to faculty of ECED : "]
    
    add_specific_ques(yml_file_path, book_name_questions, "Book Question", book_names, "books_name")
    add_specific_ques(yml_file_path, book_author_questions, "Book Question", author_names, "books_author")
    add_specific_ques(yml_file_path, book_number_questions, book_number_answers, book_names, "books_number")
    add_book_by_author_ques(yml_file_path, book_by_author_questions, "Book Question", book_names, author_names, "books_name")
    add_specific_ques(yml_file_path, faculty_location_q, faculty_location_a, faculty_names, "faculty_location")
    add_specific_ques(yml_file_path, faculty_teachings_q, faculty_teachings_a, faculty_names, "faculty_teachings")
    add_specific_ques(yml_file_path, faculty_timings_q, faculty_timings_a, faculty_names, "faculty_timings")
    add_general_ques(yml_file_path, faculty_HOD_q, faculty_HOD_a, "faculty_HOD")
    add_general_ques(yml_file_path, faculty_general_q, faculty_general_a, "faculty_general")
