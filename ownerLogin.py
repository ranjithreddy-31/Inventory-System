from workersDetails import *
from userDetails import *
from wareHouse import *
from salesDetails import *

import pyodbc
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn


def getPassword(password):
    cur, conn = getConnection()
    try:
        cur.execute("select password from userDetails")
        result = list(cur.fetchall())
        if result[0][0] == password:
            return "Success"
        else:
            return "Incorrect"

    except Exception as e:
        print(e)
    conn.close()



def getEmail(email):
    cur, conn = getConnection()
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
    cur, conn = getConnection()
    try:
        cur.execute(f"update userDetails set password = '{newPassword}' where name = 'Testuser'")
        print("Password updated successfully\n")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()
    startProgram()



def isValid(email):
    if re.fullmatch(regex, email):
        return True
    else:
        print("Invalid email format!!!")
        return False


def resetPassword():
    enter_registered_email = input("Enter your registered email: ")
    if isValid(enter_registered_email):
        if getEmail(enter_registered_email) == "Success":
            while True:
                new_password = input("Enter the new password: ")
                confirm_password = input("Reenter to confirm password: ")
                if new_password == confirm_password:
                    updatePassword(new_password)
                    break
                else:
                    print("Passwords didn't match\n")
        else:
            print("Email is not correct")
            trychoice = input("\nDo you want to try again?"
                              " Press 1 to retry or"
                              " Press any other other key to quit: ")
            if trychoice == '1':
                resetPassword()
            else:
                print("\nBye Bye! See you later")
    else:
        trychoice = input("\nDo you want to try again?"
                          " Press 1 to retry or"
                          " Press any other other key to quit: ")
        if trychoice == '1':
            resetPassword()
        else:
            print("\nBye Bye! See you later")


def displayMenu():
    print("-----------Menu-----------")
    print("1.Warehouse")
    print("2.Salesperson Details")
    print("3.Sales and Invoices")
    print("4.User Registration")
    print("5.Quit")

    print()
    print()
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

def startProgram():
    password = input("                   Welcome! \n"
                     "Enter your password to continue or Press 1 to quit: ")

    if password == '1':
        print("Thank you")
    else:
        passwordStatus = getPassword(password)
        if passwordStatus == "Success":
            menuStatus = displayMenu()
            if menuStatus == "exit":
                print("Thank you!")
        else:
            print("Incorrect password\n")
            isReset = input("Do you want to reset the password? \nPress 1 to reset or"
                            " Press any other other key to quit: ")
            if isReset.lower() == "1":
                resetPassword()
            else:
                print("Try again later by entering the correct password!")

startProgram()

