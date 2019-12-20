import psycopg2
# from theapp import app
# import viz
# from flask import render_template, request
#import pandas as pd     #We don't have pandas yet.
#We need to get some input things


#y_n = request.args.get('all_or_none', default = None, type = str)
#qst = request.args.get('question'   , default = None, type = str)
# subset by dropdown
y_n = 'yes'
qst = "Who/what are your favorite media sources that report on data science topics?"

question_to_column = {"Which of the following relational database products do you use on a regular basis?": 'q34',
                    'Which of the following cloud computing platforms do you use on a regular basis?' : 'q29',
                    "Which of the following natural language processing (NLP) methods do you use on a regular basis?": 'q27',
                    'Which categories of computer vision methods do you use on a regular basis?': 'q26',
                    'Which categories of ML tools do you use on a regular basis?' : 'q25' ,
                    'Which of the following ML algorithms do you use on a regular basis?': 'q24',
                    'What programming languages do you use on a regular basis?': 'q18',
                    "Which of the following integrated development environments (IDE's) do you use on a regular basis?": 'q16',
                    "What is the primary tool that you use at work or school to analyze data?": 'q14',
                    "On which platforms have you begun or completed data science courses?" : 'q13',
                    "Who/what are your favorite media sources that report on data science topics?": 'q12',
                    "Select any activities that make up an important part of your role at work": 'q9'}

other_questions = ['q9', 'q12', 'q14', 'q15', 'q16', 'q18', 'q24', 'q25', 'q26', 'q27', "q29", 'q34']

# q14 is all free response so all or none are equivalent.

question_size = {'q34': 12,
                 'q29': 12,
                 'q27': 6,
                 'q26': 7,
                 'q25': 8,
                 'q24': 12,
                 'q18': 12,
                 'q16': 12,
                 'q14': 5,
                 'q13': 12,
                 'q12': 12,
                 'q9': 8 }

# Initialization code to be able to query the database
conn = psycopg2.connect("dbname=kaggle user=abucklin")
cur = conn.cursor()

def query_generator_and_data_grabber(question = qst, yes_or_no = y_n):
    qnum = question_to_column[qst]
    columns = []
    for i in range(1, question_size[qnum]+1):
        string = qnum + "_" + str(i)
        columns.append(string)

    columns = columns.replace( "]" , "'").replace("[", '').replace("'", '')

    basic = "SELECT " + columns + " FROM mcq "
    conditions = ''
    query = basic + conditions + ";"
    cur.execute(query)
    data = cur.fetchall()

    if "y" in yes_or_no :
        second = "SELECT " + str(qnum) + "FROM other_questions"
        cur.execute(second + ";")
        x = cur.fetchall()
        data = data.extend(x)
    return data


raw_data = query_generator_and_data_grabber()

#data = pd.DataFrame(raw_data, columns = [in_ss , in_pp])    #Still don't have pandas.
