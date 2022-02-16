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

def getPassword():
    
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute("select password from userDetails")
        result = list(cur.fetchall())
        if result[0][0] == 'sample':
            print("Success")
            return "Success"
        else:
            return "Incorrect"

    except Exception as e:
        print(e)
    conn.close()


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


password = input("Welcome ! Enter your password to continue: ")
if getPassword() == "Success":
    if displayMenu() == "exit":
        print("Thank you!")

else:
    print("Incorrect password")
