#I developed a Flask application/website to complete this project. Programming languages used were Python, SQL, HTML, CSS, and Javascript. Storage is in a Sqlite3 database. 
import random
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#Connects to sqlite3 database
sql_connect = sqlite3.connect('questions.sqlite3', check_same_thread = False)

cursor = sql_connect.cursor()

#Gets all the tables for each type of question: multiple choice, True/False, fill-in-the-blank, and dropdown
MCQTable = cursor.execute("SELECT * FROM MCQ;").fetchall()
TFTable = cursor.execute("SELECT * FROM TFQ;").fetchall()
FITBTable = cursor.execute("SELECT * FROM FITB;").fetchall()
DTable = cursor.execute("SELECT * FROM Dropdown;").fetchall()

#Home Page
@app.route("/")
def index():
    return render_template("index.html")

#Page which shows all the questions, answer choices, and answers for viewing by the user. Passes in the tables with each type of question into the template
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
    #Chooses a random number between 0 and 19 to be the index of a MCQ question in the MCQ table
    x = random.choice(num_list)
    num_list.remove(x)

    list1 = list(range(0, 10))
    #Chooses a random number between 0 and 9 to be the index of a True/False, Fill-In-The-Blank, and Dropdown question
    y = random.choice(list1)
    list1.remove(y)

    #Gets the MCQ question, all the answer choices, and the correct answer and stores them in a list
    global MCQ
    MCQ = []
    for i in range(6):
        MCQ.append(str(MCQTable[x][i+1]))

    #Gets the TFQ question and its correct answer and stores them in a list
    global TFQ
    TFQ = []
    for i in range(2):
        TFQ.append(str(TFTable[y][i+1]))

    #Gets the Fill-In-The-Blank question and its correct answer and stores them in a list
    global FITB
    FITB = []
    for i in range(2):
        FITB.append(str(FITBTable[y][i+1]))

    #Gets the Dropdown question, all the answer choices, and the correct answer and stores them in a list
    global Dropdown
    Dropdown = []
    for i in range(6):
        Dropdown.append(str(DTable[y][i]))

    #Chooses a random question type for the 5th question
    question_type = ["MCQ", "TFQ", "FITB", "Dropdown"]
    global randomQ
    randomQ = random.choice(question_type)    

    #Based on what the fifth question was, it stores in the corresponding list the question, answer choices, and the correct answer
    if randomQ == "MCQ":
        #Chooses a random number to be the index of the 5th question
        a = random.choice(num_list)

        global MCQ1
        MCQ1 = []
        for i in range(6):
            MCQ1.append(str(MCQTable[a][i+1]))

        return render_template("test.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, MCQ1=MCQ1)
    else:
        #Chooses a random number to be the index of the 5th question
        b = random.choice(list1)

        if randomQ == "TFQ":
            global TFQ1

            TFQ1 = []
            for i in range(2):
                TFQ1.append(str(TFTable[b][i+1]))

            return render_template("test.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, TFQ1=TFQ1)

        elif randomQ == "FITB":
            global FITB1

            FITB1 = []
            for i in range(2):
                FITB1.append(str(FITBTable[b][i+1]))

            return render_template("test.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, FITB1=FITB1)

        else:
            global Dropdown1
            
            Dropdown1 = []
            for i in range(6):
                Dropdown1.append(str(DTable[b][i]))

            return render_template("test.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, Dropdown1=Dropdown1)

#Page which shows your score after the test
@app.route("/score")
def score():
    #Returns all the questions, answer choices, and correct answers that were on the test. Also returns what type of question that 5th question was.
    if randomQ == "MCQ":
        return render_template("score.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, MCQ1=MCQ1)
    elif randomQ == "TFQ":
        return render_template("score.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, TFQ1=TFQ1)
    elif randomQ == "FITB":
        return render_template("score.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, FITB1=FITB1)
    else:
        return render_template("score.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, Dropdown1=Dropdown1)

#Runs the app
if __name__ == "__main__":
    app.run(debug = True)

#Closes the connection to the sqlite3 database
sql_connect.close()
