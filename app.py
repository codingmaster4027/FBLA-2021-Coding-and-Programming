#I developed a Flask application/website to complete this project. Programming languages used were Python, SQL, HTML, CSS, 
#and Javascript. Storage is in a Sqlite3 database and there is a dynamic backup feature using a Sqlite backup API. 
import random
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#Lines 10-11, 17-18 come from the Python documentation: https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup
def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')

#Connects to sqlite3 database and creates backup database
sql_connect = sqlite3.connect('questions.sqlite3', check_same_thread = False)
backup = sqlite3.connect('backup.sqlite3', check_same_thread=False)

with backup:
    sql_connect.backup(backup, pages=1, progress=progress)

try:
    cursor = sql_connect.cursor()
except:
    cursor = backup.cursor()

#Passcode to see the database
passcode = "None"

#Counts how many times the a new passcode is generated
db_counter = 0

#Gets all the tables for each type of question: multiple choice, True/False, fill-in-the-blank, and dropdown
MCQTable = cursor.execute("SELECT * FROM MCQ;").fetchall()
TFTable = cursor.execute("SELECT * FROM TFQ;").fetchall()
FITBTable = cursor.execute("SELECT * FROM FITB;").fetchall()
DTable = cursor.execute("SELECT * FROM Dropdown;").fetchall()

#Login page
@app.route("/")
def login():
    return render_template("login.html")

#Home Page, passes in the database password to display on the home page
@app.route("/home")
def index():
    return render_template("index.html", passcode=passcode)

#Page which returns the page where the user has the enter the correct password in order to access the database. However, if the user has 
#not taken the test yet, they can access the database directly without a password. 
@app.route("/database", methods=["POST", "GET"])
def database():
    if request.method == "POST":
        user_passcode = request.form["passcode"]

        if user_passcode == passcode:
            return redirect(url_for("actualdatabase"))
        else:
            return redirect(url_for("error"))
    else:
        if db_counter == 0:
            return redirect(url_for("actualdatabase"))
        else:
            return render_template("passcode.html", passcode=passcode)

#Page which shows all the questions, answer choices, and answers for viewing by the user. Passes in the tables with each type of 
#question into the template
@app.route("/actualdatabase")
def actualdatabase():
    return render_template("database.html", MCQTable = MCQTable, TFTable = TFTable, FITBQ=FITBTable, Dropdown=DTable)

#Error message page if the user entered the wrong password for the database passcode page
@app.route("/error")
def error():
    return render_template("error.html")

#Test instructions page
@app.route("/beforetest")
def beforetest():
    return render_template("beforetest.html")

#Page with the actual test
@app.route("/test")
def test():
    #Function which creates the fifth question on the test (which is of a random question type) and returns the test page
    def question5(index=None):
        global q5
        
        #List which is going to contain the question, answer choices, and answer
        q5 = []

        #Fills the list with its contents based on the question type of the 5th question
        if randomQ == "MCQ":
            global MCQIndices

            MCQIndices.remove(MCQIndex)

            q5Index = random.choice(MCQIndices)

            for i in range(6):
                q5.append(str(MCQTable[q5Index][i+1]))

        else:
            global nonMCQIndices

            nonMCQIndices.remove(indices[index])

            q5Index = random.choice(nonMCQIndices)

            if randomQ == "TFQ":
                for i in range(2):
                    q5.append(str(TFTable[q5Index][i+1]))

            elif randomQ == "FITB":
                for i in range(2):
                    q5.append(str(FITBTable[q5Index][i+1]))

            else:
                for i in range(6):
                    q5.append(str(DTable[q5Index][i]))

        #Returns the test page
        return render_template("test.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, q5=q5)
    
    global passcode
    global db_counter

    #Increases db_counter by 1
    db_counter += 1

    #Creates a new-random 9-digit passcode
    for i in range(9):
        if i == 0:
            passcode = str(random.randint(0, 9))
        else:
            passcode += str(random.randint(0, 9))

    global MCQIndices

    MCQIndices = list(range(0, 20))
    #Chooses a random number between 0 and 19 to be the index of an MCQ question in the MCQ table to be asked on the test.
    global MCQIndex
    
    MCQIndex = random.choice(MCQIndices)

    global nonMCQIndices
    nonMCQIndices = list(range(0, 10))
    #Chooses a random number between 0 and 9 to be the index of a True/False, Fill-In-The-Blank, and Dropdown question.
    global indices
    indices = []

    for _ in range(3):
        q234Indices = random.choice(nonMCQIndices)
        indices.append(q234Indices)

    #Gets the questions, all the answer choices, and the correct answer and stores them in the corresponding lists
    global MCQ
    MCQ = []

    global TFQ
    TFQ = []

    global FITB
    FITB = []

    global Dropdown
    Dropdown = []

    for i in range(6):
        MCQ.append(str(MCQTable[MCQIndex][i+1]))
        Dropdown.append(str(DTable[indices[2]][i]))
        
        if i < 2:
            TFQ.append(str(TFTable[indices[0]][i+1]))
            FITB.append(str(FITBTable[indices[1]][i+1]))

    #Chooses a random question type for the 5th question
    question_type = ["MCQ", "TFQ", "FITB", "Dropdown"]
    global randomQ
    randomQ = random.choice(question_type)    

    #Based on what the fifth question was, it returns/renders the appropriate template with the question5() function. 
    if randomQ == "MCQ":
        return question5()

    elif randomQ == "TFQ":
        return question5(0)

    elif randomQ == "FITB":
        return question5(1)

    else:
        return question5(2)

#Page which shows your score after the test
@app.route("/score")
def score():
    return render_template("score.html", randomQ=randomQ, MCQ=MCQ, TFQ=TFQ, FITB=FITB, Dropdown=Dropdown, q5=q5, passcode=passcode)

#Q & A Page with the interactive chatbot and FAQ
@app.route("/qa")
def qa():
    return render_template("qa.html")

#Runs the app
if __name__ == "__main__":
    app.run(debug = True)

#Closes the connection to the sqlite3 database
sql_connect.close()
backup.close()
