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
        file.write("categories:\n- {}\n".format(category))
        file.write("conversations:\n\n")

def isList(var):
    return type(var) == type([])

def fetch_index(file_path, data, category, category_knowledge=False):
    """fetches the index of category in the 'data' list provided"""
    if not category_knowledge:
    # if you dont know about the category's existence in the yml file
    # check handle the condition where it does not exist and change the file
        try:
            req_index = data.index("- " + category + "\n") + 2
        except ValueError:
            add_category(file_path, category)
            data = read_data(file_path)
            req_index = data.index("- " + category + "\n") + 2
        return req_index, data
    else:
        req_index = data.index("- " + category + "\n") + 2
        return req_index

def read_excel(file_path, first_col_names = True):
    """reads an excel file (with one sheet) and returns the data"""
    file_path = r"{}".format(file_path)
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(0)
    data = {}
    if first_col_names:
        col_names = []
        for i in range(sheet.ncols):
            col_names.append(sheet.cell_value(0, i))
        for col in col_names:
            data[col] = []
        for i in range(sheet.ncols):
            col = col_names[i]
            for j in range(1, sheet.nrows):
                data[col].append(sheet.cell_value(j, i))
    else:
        for i in range(sheet.ncols):
            data[i] = []
            for j in range(sheet.nrows):
                data[i].append(sheet.cell_value(j, i))
    return data

def read_excel_mult_sheets(file_path):
    """project specific function to read data from multiple sheets of an excel file"""
    file_path = r"{}".format(file_path)
    wb = xlrd.open_workbook(file_path)
    sheet_names = wb.sheet_names()
    data = {}
    col_indices = [0, 1] #column indices in each sheet to be fetched
    col_names = ["book_name", "author_name"]
    for col_name in col_names:
        data[col_name] = []
        # we do this since all the sheets have the same type of data in the corresponding columns.
        # Hence appending data across the sheets wont have any negative effect
    for ind in range(len(sheet_names)):
        sheet = wb.sheet_by_index(ind)
        for i in range(2):
            for j in range(sheet.nrows):
                data[col_names[i]].append(sheet.cell_value(j, col_indices[i]))
    for col_name in col_names:
        data[col_name] = [ele for ele in data[col_name] if ele not in ['', '**', '-', 'NA']]
        #remove empty entries, cant be used for conversation
        data[col_name] = list(set(data[col_name]))
        #remove duplicate elements, showing all entries related to this element would be better
    data["categories"] = sheet_names
    return data

def add_gen_ques(yml_file_path, questions, answers, category):
    """adds general questions to the YML file"""
    data = read_data(yml_file_path)
    req_index, data = fetch_index(yml_file_path, data, category)
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    ins = data.insert
    #doing this to try and decrease runtime of program.
    # Dot function calls take up a lot more time as per the python wiki page
    [ins(req_index, "- - {}\n  - {}\n".format(questions[i], answers[i % len(answers)])) for i in range(len(questions))]
    # for i in range(len(questions)):
    #     ins(req_index, "- - {}\n".format(questions[i]))
    #     ins(req_index+1, "  - {}\n".format(answers[i%len(answers)]))
    write_data(yml_file_path, data)

def add_spec_ques(yml_file_path, questions, answers, names, category):
    """adds specific questions to the YML file where placeholder in given question format is substitued with provided names"""
    data = read_data(yml_file_path)
    req_index, data = fetch_index(yml_file_path, data, category)
    qstns = []
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    for name in names:
        temp = [question.replace("_", name) for question in questions]
        qstns.extend(temp)
    questions = qstns
    ins = data.insert
    [ins(req_index, "- - {}\n  - {}\n".format(questions[i], answers[i % len(answers)])) for i in range(len(questions))]
    # for i in range(len(questions)):
    #     ins(req_index, "- - {}\n".format(questions[i]))
    #     ins(req_index+1, "  - {}\n".format(answers[i%len(answers)]))
    write_data(yml_file_path, data)

def add_book_author_ques(yml_file_path, questions, answers, book_names, author_names, category):
    """adds questions containing both book names and author names to the YML file via substituting two placeholders in the question format"""
    data = read_data(yml_file_path)
    req_index, data = fetch_index(yml_file_path, data, category)
    if not isList(questions):
        questions = [questions]
    if not isList(answers):
        answers = [answers]
    temp = []
    temp2 = []
    for book in book_names:
        temp = [question.replace("_", book, 1) for question in questions]
        for author in author_names:
            temp2.extend([question.replace("_", author) for question in temp])
    questions = temp2
    ins = data.insert
    [ins(req_index, "- - {}\n  - {}\n".format(questions[i], answers[i%len(answers)])) for i in range(len(questions))]
    # list comprehension version for the for-loop. Better performance?
    # for i in range(len(questions)):
    #     ins(req_index, "- - {}\n".format(questions[i]))
    #     ins(req_index+1, " - {}\n".format(answers[i%len(answers)]))
    write_data(yml_file_path, data)

def extract_qna(data, start_index):
    """prepares lists of questions and answers in the given yml file"""
    questions = []
    answers = []
    end_index = -1
    for i in range(start_index, len(data)-1):
        if "categories:" in data[i]:
            end_index = i
            break
        if "- - " in data[i]:
            questions.append(data[i])
            answers.append(data[i+1])
    return questions, answers, end_index

def delete_duplicates(yml_file_path, categories):
    """deletes the duplicate questions and the corresponding answers in YML file"""
    data = read_data(yml_file_path)
    for category in categories:
        req_index = fetch_index(yml_file_path, data, category, True)
        questions, answers, end_index = extract_qna(data, req_index)
        ques = list(dict.fromkeys(questions))
        ans = answers[:len(ques)]
        if not (len(ques) == 0 | len(ans) == 0):
            qna_list = ['\n{}{}'.format(ques[i], ans[i]) for i in range(len(ques))]
        if end_index != -1:
            data = data[:req_index] + qna_list + data[end_index:]
        else:
            data = data[:req_index] + qna_list
    write_data(yml_file_path, data)

if __name__ == "__main__":
    excel_file_path = 'faculties.xlsx'#input("Excel file path (for the faculty information) : ")
    excel_lib_file_path = 'ProcessedLib.xlsx'#input("Excel file path (for the library database) : ")
    excel_sub_file_path = 'Abbrevations.xlsx'#input("Excel file path (for the abbreviations) : ")
    yml_file_path = 'test_yml.yml'#input("Target YML file path : ")
    excel_dict = read_excel(excel_file_path)
    excel_lib_dict = read_excel_mult_sheets(excel_lib_file_path)
    excel_sub_dict = read_excel(excel_sub_file_path, False)
    faculty_names = excel_dict["Faculty"]
    book_names = excel_lib_dict["book_name"]
    author_names = excel_lib_dict["author_name"]
    categories = excel_lib_dict["categories"]
    faculty_code_names = excel_dict["Code"]
    subject_full_names = excel_sub_dict[1]

    faculty_names.extend(faculty_code_names)
    book_subject_questions = ["Books for _", "Books on _", "_ books"]
    book_name_questions = ["is _ available in the library?", "Is the book _ there?", "Any book named _?", "Can you search for the availability of _?",
                           "Can I get the book _?", "Do you have _?"]
    book_number_questions = ["How many books named _ are avaiable?","How many copies of _ are there?", "Can I know how many copies of _ are there?",
                             "Number of books of _?", "Number of _  books?", "_ book number", "Books number of _", "How many _ books are there?",
                             "Count of _"]
    book_number_answers = ["As per the inventory, there are: ", "Let me peek through... There are: ", "The number books available are:",
                            "Yes, the number is: ", "There must be around: "]
    book_author_questions = ["What all are the books written by _?", "Books written by _?", "Books of _?", "Which of _'s books are available?",
                             "Can I get any of _'s books?", "Can you search for the availability of book written by _?", "Can I get books of _?",
                             "_'s books"]

    book_by_author_questions = ["is _ by _ available?", "_ by _", "_ book by _", "_ written by _", "_ of _", "_ book of _"]

    faculty_location_q = ["is _ in the office?", "Where does _ sit?", "Where is _'s cabin?","Where does _ reside in the department?",
                        "Where can I meet _?", "Is _ in the department?", "Where can I find _?", "Where is _", "Cabin of _", "Place of _", "_'s cabin"]
    faculty_location_a = ["let me check the database for that: ", "I have to check the database for that. Please wait: ",
                          "Kindly wait while I check the database: "]
    faculty_teachings_q = ["Which subject does _ teach?", "Which classes does _ take?","Does _ teach DCN?", "Subjects taught by _",
                         "What are _'s specializations?", "What are the specializations of _?", "Which subjects are taught by _?",
                           "Can I get the list of subjects taken by _?", "Subjects taught by _", "Specializations of _", "Subjects by _",
                           "What _ teaches?", "What _ tells?", "What subjects _ takes?", "Will _ teach VLSI?", "Is AIC taught by _?", "What does _ teach?",
                           "What subjects does _ take?"]
    faculty_teachings_a = ["Accessing faculty database: ", "The details you need are as follows : ", "Here are the requested details: "]
    faculty_timings_q = ["When is _ available?", "Timings of _'s availability", "Till when is _ in department?", "When can I meet _?", "Can I meet _ now?",
                         "Can I meet _?", "When will _ leave?", "When can I visit _?", "Is _ currently available?", "Is _ there?", "_'s availability",
                         "When will _ be?", "Timings of _"]
    faculty_timings_a = ["Here are your details, please note that these might be incorrect: ", "Requested timing details are as follows : "]
    faculty_general_q = ["Who are the professors in the department?", "Who are the asst. professors in the department?",
                         "Who are the teaching assistants in the department?", "Who is the HOD?", "Who is the Head of the Department?"]
    faculty_general_a = ["Presenting the information requested : ", "Details needed are as follows : "]
    categories = ["books_name", "books_author", "books_number", "faculty_location", "faculty_teachings", "faculty_timings", "faculty_general"]

    add_spec_ques(yml_file_path, book_name_questions, "Book Question", book_names, "books_name")
    add_spec_ques(yml_file_path, book_author_questions, "Book Question", author_names, "books_author")
    add_book_author_ques(yml_file_path, book_by_author_questions, "Book Question", book_names, author_names, "books_name")
    add_spec_ques(yml_file_path, book_number_questions, book_number_answers, book_names, "books_number")
    add_spec_ques(yml_file_path, book_subject_questions, "Book Question", subject_full_names, "books_name")
    add_spec_ques(yml_file_path, faculty_location_q, faculty_location_a, faculty_names, "faculty_location")
    add_spec_ques(yml_file_path, faculty_teachings_q, faculty_teachings_a, faculty_names, "faculty_teachings")
    add_gen_ques(yml_file_path, "Where is the HOD's cabin?", faculty_location_a[0], "faculty_location")
    add_spec_ques(yml_file_path, faculty_timings_q, faculty_timings_a, faculty_names, "faculty_timings")
    add_gen_ques(yml_file_path, faculty_general_q, faculty_general_a, "faculty_general")
    delete_duplicates(yml_file_path, categories)
