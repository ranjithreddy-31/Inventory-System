from workersDetails import WorkerDetails
from wareHouse import WareHouse
from salesDetails import SalesDetails

import pyodbc
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

class OwnerLogin:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-VU4ECPI;'
                            'Database=praneeth;'
                            'Trusted_Connection=yes;')
        cur = conn.cursor()
        return cur, conn


    def getPassword(self, password):
        cur, conn = self.getConnection()
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



    def getEmail(self, email):
        cur, conn = self.getConnection()
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


    def updatePassword(self, newPassword):
        cur, conn = self.getConnection()
        try:
            cur.execute(f"update userDetails set password = '{newPassword}' where name = 'Testuser'")
            print("Password updated successfully\n")
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()
        self.startProgram()



    def isValid(self, email):
        if re.fullmatch(regex, email):
            return True
        else:
            print("Invalid email format!!!")
            return False


    def resetPassword(self):
        enter_registered_email = input("Enter your registered email: ")
        if self.isValid(enter_registered_email):
            if self.getEmail(enter_registered_email) == "Success":
                while True:
                    new_password = input("Enter the new password: ")
                    confirm_password = input("Reenter to confirm password: ")
                    if new_password == confirm_password:
                        self.updatePassword(new_password)
                        break
                    else:
                        print("Passwords didn't match\n")
            else:
                print("Email is not correct")
                trychoice = input("\nDo you want to try again?"
                                " Press 1 to retry or"
                                " Press any other other key to quit: ")
                if trychoice == '1':
                    self.resetPassword()
                else:
                    print("\nBye Bye! See you later")
        else:
            trychoice = input("\nDo you want to try again?"
                            " Press 1 to retry or"
                            " Press any other other key to quit: ")
            if trychoice == '1':
                self.resetPassword()
            else:
                print("\nBye Bye! See you later")


    def displayMenu(self):
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
            warehouse = WareHouse()
            warehouse.wareHouse()
        elif workflowNumber == 2:
            workerdetails = WorkerDetails()
            workerdetails.workerDetails()
        elif workflowNumber == 3:
            salesdetails = SalesDetails()
            salesdetails.salesDetails()
        elif workflowNumber == 4:
            from userDetails import UserDetails
            userdetails = UserDetails()
            userdetails.userDetails()
        elif workflowNumber == 5:
            return "exit"
        return "exit"

    def startProgram(self):
        password = input("                   Welcome! \n"
                        "Enter your password to continue or Press 1 to quit: ")

        if password == '1':
            print("Thank you")
        else:
            passwordStatus = self.getPassword(password)
            if passwordStatus == "Success":
                menuStatus = self.displayMenu()
                if menuStatus == "exit":
                    print("Thank you!")
            else:
                print("Incorrect password\n")
                isReset = input("Do you want to reset the password? \nPress 1 to reset or"
                                " Press any other other key to quit: ")
                if isReset.lower() == "1":
                    self.resetPassword()
                else:
                    print("Try again later by entering the correct password!")

ownerlogin = OwnerLogin() 
ownerlogin.startProgram()

