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
        from wareHouse import WareHouse
        warehouse = WareHouse()
        warehouse.wareHouse()
    elif workflowNumber == 2:
        from workersDetails import WorkerDetails
        workerdetails = WorkerDetails()
        workerdetails.workerDetails()
    elif workflowNumber == 3:
        from salesDetails import SalesDetails
        salesdetails = SalesDetails()
        salesdetails.salesDetails()
    elif workflowNumber == 4:
        from userDetails import UserDetails
        userdetails = UserDetails()
        userdetails.userDetails()
    elif workflowNumber == 5:
        return "exit"
    return "exit"
