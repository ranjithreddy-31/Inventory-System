import commonFunctions
import pyodbc
from prettytable import PrettyTable


def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-VU4ECPI;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn


def showWorkerDetails():
    cur, conn = getConnection()

    try:
        cur.execute("select * from salesPersonDetails")
        results = cur.fetchall()
        x = PrettyTable()
        x.field_names = [i[0] for i in cur.description]
        for row in results:
            x.add_row(list(row))
        print(x)

    except Exception as e:
        print(e)
    conn.commit()
    conn.close()
    workerDetails()


def checkUserExists(id):
    cur, conn = getConnection()
    try:
        cur.execute(f"select 1 from salesPersonDetails where person_id = {id}")
        results = cur.fetchall()
        conn.commit()
        conn.close()
        if len(results) > 0:
            return True
        return False
    except Exception as e:
        print(e)
        conn.commit()
        conn.close()


def updateCommission():
    userId = input("Choose person id whose commission percentage need to be updated: ")
    if checkUserExists(userId):
        newPercentage = input("Enter the new commission percentage: ")
        cur, conn = getConnection()
        try:
            cur.execute(
                f"update salesPersonDetails set commission_earned = {newPercentage} where person_id = {float(userId)}")
            print("Successfully updated new percentage")

        except Exception as e:
            print(e)
        conn.commit()
        conn.close()
        workerDetails()
    else:
        print("User with that particular id doesn't exist.\n")
        userInput = input("Press 1 to enter the userId again or any other key to go back: ")
        if userInput == '1':
            updateCommission()
        else:
            workerDetails()


def workerDetails():
    print()
    print()
    print("Salespersons deails")
    print("1.Show workers details")
    print("2.Update commission percentage")
    print("Press any other key to exit to main menu")
    print()
    print()
    ware_house_input = input("Enter the number based on the operation that you want to perform: ")
    if ware_house_input == '1':
        showWorkerDetails()
    elif ware_house_input == '2':
        updateCommission()
    else:
        commonFunctions.displayMenu()

