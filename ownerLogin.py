from salesDetails import *
from workersDetails import *
from userDetails import *
from wareHouse import *

import pyodbc

def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-VU4ECPI;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    return conn


def getPassword(password):
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute("select password from userDetails")
        result = list(cur.fetchall())
        if result[0][0] == password:
            print(result[0][0])
            return "Success"
        else:
            return "Incorrect"

    except Exception as e:
        print(e)
    conn.close()



def getEmail(email):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()

    try:
        cur.execute("select email from userDetails")
        result = list(cur.fetchall())
        if result[0][0] == email:
            return "Success"
        else:
            return "Incorrect"

    except Exception as e:
        print(e)
    conn.close()


def updatePassword(newPassword):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()

    try:
        cur.execute(f"update userDetails set password = '{newPassword}' where name = 'Testuser'")
        print("Password updated successfully")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def resetPassword():
    enter_registered_email = input("Enter your registered email: ")
    if getEmail(enter_registered_email) == "Success":
        new_password = input("Enter the new password: ")
        confirm_password = input("Reenter to confirm password: ")
        if new_password == confirm_password:
            updatePassword(new_password)
        else:
            print("Passwords didn't match")


def displayMenu():
    print("-----------Menu-----------")
    print("1.Warehouse")
    print("2.Salesperson Details")
    print("3.Sales and Invoices")
    print("4.User Registration")
    print("5.Quit")
    workflowNumber = int(input("Enter the number to navigate: "))

    if workflowNumber == 1:
        wareHouse()
    elif workflowNumber == 2:
        workerDetails()
    elif workflowNumber == 3:
        salesDetails()
    elif workflowNumber == 4:
        userDetails()
    elif workflowNumber == 5:
        return "exit"
    return "exit"


password = input("Welcome! Enter your password to continue or Press 1 to quit: ")
if password == '1':
    print("Thank you")
else:
    if getPassword(password) == "Success":
        if displayMenu() == "exit":
            print("Thank you!")
    else:
        print("Incorrect password")
        isReset = input("Do you want to reset the password? Yes/No: ")
        if isReset.lower() == "yes":
            resetPassword()
        else:
            print("Try again by entering the correct password!")

