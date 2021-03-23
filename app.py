#I developed a Flask application/website to complete this project. Programming languages used were Python, SQL, HTML, CSS, and Javascript. Storage is in a Sqlite3 database. 
import random
from flask import Flask, redirect, render_template, request, session, url_for
import sys; sys.path
import sqlite3

app = Flask(__name__)

#Connects to sqlite database
sql_connect = sqlite3.connect('questions.sqlite3', check_same_thread = False)

cursor = sql_connect.cursor()

#Gets all the tables for each type of question
MCQTable = cursor.execute("SELECT * FROM MCQ;").fetchall()
TFTable = cursor.execute("SELECT * FROM TFQ;").fetchall()
FITBTable = cursor.execute("SELECT * FROM FITB;").fetchall()
DTable = cursor.execute("SELECT * FROM Dropdown;").fetchall()

#Home Page
@app.route("/")
def index():
    return render_template("index.html")

#Page which shows all the questions
@app.route("/database")
def database():
    return render_template("database.html", MCQTable = MCQTable, TFTable = TFTable, FITBQ=FITBTable, Dropdown=DTable)

#Test instructions page
@app.route("/beforetest")
def beforetest():
    return render_template("beforetest.html")

#Page with the actual test
@app.route("/test")
def test():
    num_list = list(range(0, 20))
    global x
    #Chooses a random number between 0 and 19 to be the index of a MCQ question in the MCQ table
    x = random.choice(num_list)
    num_list.remove(x)

    list1 = list(range(0, 10))
    global y
    #Chooses a random number between 0 and 9 to be the index of a True/False, Fill-In-The-Blank, and Dropdown question
    y = random.choice(list1)
    list1.remove(y)

    #Chooses a random question type for the 5th question
    question_type = ["MCQ", "TFQ", "FITB", "Dropdown"]
    global randomQ
    randomQ = random.choice(question_type)
    global a
    a = random.choice(num_list)
    global b
    b = random.choice(list1)

    #Gets the MCQ question, all the answer choices, and the correct answer and stores them in variables
    MCQQ = str(MCQTable[x][1])
    MCQA = str(MCQTable[x][2])
    MCQB = str(MCQTable[x][3])
    MCQC = str(MCQTable[x][4])
    MCQD = str(MCQTable[x][5])
    MCQCorrect = str(MCQTable[x][6])

    #Gets the TFQ question and its correct answer and stores them in variables
    TFQ = str(TFTable[y][1])
    TFCorrect = str(TFTable[y][2])

    #Gets the Fill-In-The-Blank question and its correct answer and stores them in variables
    FITBQ = str(FITBTable[y][1])
    FITBCorrect = str(FITBTable[y][2])

    #Gets the Dropdown question, all the answer choices, and the correct answer and stores them in variables
    DQ = str(DTable[y][0])
    D1 = str(DTable[y][1])
    D2 = str(DTable[y][2])
    D3 = str(DTable[y][3])
    D4 = str(DTable[y][4])
    DCorrect = str(DTable[y][5])

    #Based on what the fifth question was, it stores in variables the question, answer choices, and the correct answer
    if randomQ == "MCQ":
        MCQQ1 = str(MCQTable[a][1])
        MCQA1 = str(MCQTable[a][2])
        MCQB1 = str(MCQTable[a][3])
        MCQC1 = str(MCQTable[a][4])
        MCQD1 = str(MCQTable[a][5])
        MCQCorrect1 = str(MCQTable[a][6])
        TFQ1 = None
        TFCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    elif randomQ == "TFQ":
        TFQ1 = str(TFTable[b][1])
        TFCorrect1 = str(TFTable[b][2])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    elif randomQ == "FITB":
        FITBQ1 = str(FITBTable[b][1])
        FITBCorrect1 = str(FITBTable[b][2])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        TFQ1 = None
        TFCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    else:
        DQ1 = str(DTable[b][0])
        D11 = str(DTable[b][1])
        D21 = str(DTable[b][2])
        D31 = str(DTable[b][3])
        D41 = str(DTable[b][4])
        DCorrect1 = str(DTable[b][5])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        TFQ1 = None
        TFCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None

    return render_template("test.html", MCQ=MCQQ, A=MCQA, B=MCQB, C=MCQC, D=MCQD, TFQ=TFQ, FITBQ=FITBQ, DQ=DQ, D1=D1, D2=D2, D3=D3, D4=D4, MCQQ1=MCQQ1, MCQA1=MCQA1, MCQB1=MCQB1, MCQC1=MCQC1, MCQD1=MCQD1, TFQ1=TFQ1, FITBQ1=FITBQ1, DQ1=DQ1, D11=D11, D21=D21, D31=D31, D41=D41, randomQ=randomQ, MCQCorrect=MCQCorrect, MCQCorrect1=MCQCorrect1, FITBCorrect=FITBCorrect, FITBCorrect1=FITBCorrect1, DCorrect=DCorrect, DCorrect1=DCorrect1, TFCorrect=TFCorrect, TFCorrect1=TFCorrect1)

#Page which shows your score after the test
@app.route("/score")
def score():
    #Returns all the questions, answer choices, and correct answers that were on the test
    MCQQ = str(MCQTable[x][1])
    MCQA = str(MCQTable[x][2])
    MCQB = str(MCQTable[x][3])
    MCQC = str(MCQTable[x][4])
    MCQD = str(MCQTable[x][5])
    MCQCorrect = str(MCQTable[x][6])

    TFQ = str(TFTable[y][1])
    TFCorrect = str(TFTable[y][2])

    FITBQ = str(FITBTable[y][1])
    FITBCorrect = str(FITBTable[y][2])

    DQ = str(DTable[y][0])
    D1 = str(DTable[y][1])
    D2 = str(DTable[y][2])
    D3 = str(DTable[y][3])
    D4 = str(DTable[y][4])
    DCorrect = str(DTable[y][5])

    if randomQ == "MCQ":
        MCQQ1 = str(MCQTable[a][1])
        MCQA1 = str(MCQTable[a][2])
        MCQB1 = str(MCQTable[a][3])
        MCQC1 = str(MCQTable[a][4])
        MCQD1 = str(MCQTable[a][5])
        MCQCorrect1 = str(MCQTable[a][6])
        TFQ1 = None
        TFCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    elif randomQ == "TFQ":
        TFQ1 = str(TFTable[b][1])
        TFCorrect1 = str(TFTable[b][2])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    elif randomQ == "FITB":
        FITBQ1 = str(FITBTable[b][1])
        FITBCorrect1 = str(FITBTable[b][2])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        TFQ1 = None
        TFCorrect1 = None
        DQ1 = None
        D11 = None
        D21 = None
        D31 = None
        D41 = None
        DCorrect1 = None

    else:
        DQ1 = str(DTable[b][0])
        D11 = str(DTable[b][1])
        D21 = str(DTable[b][2])
        D31 = str(DTable[b][3])
        D41 = str(DTable[b][4])
        DCorrect1 = str(DTable[b][5])
        MCQQ1 = None
        MCQA1 = None
        MCQB1 = None
        MCQC1 = None
        MCQD1 = None
        MCQCorrect1 = None
        TFQ1 = None
        TFCorrect1 = None
        FITBQ1 = None
        FITBCorrect1 = None
    return render_template("score.html", MCQ=MCQQ, A=MCQA, B=MCQB, C=MCQC, D=MCQD, TFQ=TFQ, FITBQ=FITBQ, DQ=DQ, D1=D1, D2=D2, D3=D3, D4=D4, MCQQ1=MCQQ1, MCQA1=MCQA1, MCQB1=MCQB1, MCQC1=MCQC1, MCQD1=MCQD1, TFQ1=TFQ1, FITBQ1=FITBQ1, DQ1=DQ1, D11=D11, D21=D21, D31=D31, D41=D41, randomQ=randomQ, MCQCorrect=MCQCorrect, MCQCorrect1=MCQCorrect1, FITBCorrect=FITBCorrect, FITBCorrect1=FITBCorrect1, DCorrect=DCorrect, DCorrect1=DCorrect1, TFCorrect=TFCorrect, TFCorrect1=TFCorrect1)

#Runs the app
if __name__ == "__main__":
	app.run(debug = True)

sql_connect.close()