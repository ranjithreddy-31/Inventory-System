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
        import wareHouse
        wareHouse.wareHouse()
    elif workflowNumber == 2:
        import workersDetails 
        workersDetails.workerDetails()
    elif workflowNumber == 3:
        import salesDetails
        salesDetails.salesDetails()
    elif workflowNumber == 4:
        import userDetails
        userDetails.userDetails()
    elif workflowNumber == 5:
        return "exit"
    return "exit"
