import xlrd

def read_data(file_path):
    """reads data from a file and returns it"""
    file_path = r"{}".format(file_path)
    with open(file_path, "r") as file:
        data = file.read()
    return data

def add_specific_ques(file_path, question, answer, names, category):
    """adds a question to the file specified. question is expected to be in a specific format"""
    file_path = r"{}".format(file_path)
    ques_exist = check_question(file_path, question.replace("_", names[0])) #even if a sample exists, the operation has been done
    if not ques_exist:
        with open(file_path, "r") as file:
            data = file.readlines()
        try:
            req_index = data.index("- " + category + "\n") + 2
        except:
            add_category(file_path, category)
            with open(file_path, "r") as file:
                data = file.readlines()
            req_index = data.index("- " + category + "\n") + 2
        questions = [question.replace("_", name) for name in names]
        i = req_index
        for question in questions:
            data.insert(i, "\n- - {}\n  - {}".format(question, answer))
        with open(file_path, "w") as file:
            for line in data:
                file.write(line)
    else:
        print(question + " questions already exist")

def add_general_ques(file_path, question, answer, category):
    """adds a general type question to the file specified"""
    file_path = r"{}".format(file_path)
    ques_exist = check_question(file_path, question)
    if not ques_exist:
        with open(file_path, "r") as file:
            data = file.readlines()
        try:
            req_index = data.index("- " + category + "\n") + 2
        except ValueError:
            add_category(file_path, category)
            with open(file_path, "r") as file:
                data = file.readlines()
            req_index = data.index("- " + category + "\n") + 2
        data.insert(req_index, "\n- - {}\n  - {}".format(question, answer))
        with open(file_path, "w") as file:
            for line in data:
                file.write(line)
    else:
        print(question + " question already exists")

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

def extract_qna(file_path, names, category):
    """prepares common questions and answers in the given category from the yml file given for training"""
    file_path = r"{}".format(file_path)
    with open(file_path, "r") as file:
        data = file.readlines()
    req_name = names[0]
    questions = []
    answers = []
    start_index = data.index("- " + category + "\n") + 2
    for i in range(start_index, len(data)):
        if "categories:" in data[i]:
            break 
        if req_name in data[i]:
            if "- - " in data[i]:
                questions.append(data[i])
                answers.append(data[i+1])
    questions = [question.replace("- - ", "") for question in questions]
    questions = [question.replace(req_name, "_") for question in questions]
    answers = [answer.replace(req_name, "_") for answer in answers] 
    answers = [answer.replace("  - ", "") for answer in answers]
    return [questions, answers]

def add_category(file_path, category):
    """adds a category to the yml file given"""
    file_path = r"{}".format(file_path)
    with open(file_path, "a") as file:
        file.write("\ncategories:\n- {}\n".format(category))
        file.write("conversations:\n")

def check_question(file_path, question):
    """checks whether a question already exists in the yml file or not"""
    with open(file_path, "r") as file:
        data = file.readlines()
        for line in data:
            if question in line:
                return True
        return False

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
    
    #[faculty_ques, faculty_ans] = extract_qna(yml_file_path, faculty_names, "Faculty")
    book_name_questions = ["is _ available in the library?", "How many copies of _ are the?"]
    book_author_questions = ["What all are the books written by _?", "Books written by _?", "Books of _?", "Subjects _ have written books in"]
    for book_name_qstn in book_name_questions:
        add_specific_ques(yml_file_path, book_name_qstn, "Book Question", book_names, "books_name")
    for book_author_qstn in book_author_questions:
        add_specific_ques(yml_file_path, book_author_qstn, "Book Question", author_names, "books_author")
    
    #[lib_ques, lib_ans] = extract_qna(yml_file_path, book_names, "Books")
    faculty_questions = ["is _ in the office?", "Where does _ sit?", "Where is _ cabin?", "Which subject does _ teach?", "Which classes does _ take?",
                         "Does _ teach DCN?", "Subjects taught by _", "When is _ available?", "Where do the _ reside in the department?",
                         "What are _'s speciatizations?","What are the specializations of _?", "Who is the HOD?", "Who is the Head of the Department?",
                         "Where is the HOD's cabin?"]
    for faculty_qstn in faculty_questions:
        add_specific_ques(yml_file_path, faculty_qstn, "Just a breath...", faculty_names, "faculty")
