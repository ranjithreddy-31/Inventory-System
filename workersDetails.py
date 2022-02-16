import pyodbc
from prettytable import PrettyTable

def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
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


def updateCommission():
    showWorkerDetails()
    userId = input("Choose person id whose commission percentage need to be updated: ")
    newPercentage = input("Enter the new commission percentage: ")
    cur, conn = getConnection()

    try:
        cur.execute(f"update salesPersonDetails set commission_earned = {newPercentage} where person_id = {float(userId)}")
        print("Successfully updated new percentage")

    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def workerDetails():
    print("Salespersons deails")
    print("1.Show workers details")
    print("2.Update commission percentage")
    print("Press any other key to exit to main menu")
    ware_house_input = int(input("Enter the number based on the operation that you want to perform: "))
    if ware_house_input == 1:
        showWorkerDetails()
    elif ware_house_input == 2:
        updateCommission()
    else:
        # displayMenu()
        pass
