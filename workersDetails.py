import commonFunctions
import pyodbc
from prettytable import PrettyTable

class WorkerDetails:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-VU4ECPI;'
                            'Database=praneeth;'
                            'Trusted_Connection=yes;')
        cur = conn.cursor()
        return cur, conn


    def showWorkerDetails(self):
        cur, conn = self.getConnection()

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
        self.workerDetails()


    def checkUserExists(self, id):
        cur, conn = self.getConnection()
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


    def updateCommission(self):
        userId = input("Choose person id whose commission percentage need to be updated: ")
        if self.checkUserExists(userId):
            newPercentage = input("Enter the new commission percentage: ")
            cur, conn = self.getConnection()
            try:
                cur.execute(
                    f"update salesPersonDetails set commission = {newPercentage} where person_id = {float(userId)}")
                print("Successfully updated new percentage")

            except Exception as e:
                print(e)
            conn.commit()
            conn.close()
            self.workerDetails()
        else:
            print("User with that particular id doesn't exist.\n")
            userInput = input("Press 1 to enter the userId again or any other key to go back: ")
            if userInput == '1':
                self.updateCommission()
            else:
                self.workerDetails()


    def workerDetails(self):
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
            self.showWorkerDetails()
        elif ware_house_input == '2':
            self.updateCommission()
        else:
            commonFunctions.displayMenu()

