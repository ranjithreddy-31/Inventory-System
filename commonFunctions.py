from workersDetails import *
from wareHouse import *
from salesDetails import *
from userDetails import *


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
