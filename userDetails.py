import commonFunctions
import pyodbc
from prettytable import PrettyTable
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UserDetails:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-VU4ECPI;'
                            'Database=praneeth;'
                            'Trusted_Connection=yes;')
        cur = conn.cursor()
        return cur, conn

    def isValid(self, email):
        if re.fullmatch(regex, email):
            return True
        else:
            print("Invalid email format!!!")
            return False

    def displayMenu(self):
        choice = int(input('1. Add new Customer\n2. Get Customer Details\n3. Show all Customer Details\n4. Delete Customer Details\n5. Quit \n\nChoose '
                        'an option: '))
        cursor, conn = self.getConnection()
        if choice == 1:
            try:
                cursor.execute('select max(customerID) from customerDetails;')
                res = cursor.fetchall()[0]
                if res[0]:
                    max_id = int(res[0])+1
                else:
                    max_id = 1
                
                name = input('Enter the name of Customer: ')
                zip = int(input('Enter the ZIP code of customer: '))
                tax_rate = int(input('Enter the tax percentage: '))
                email = input('Enter the email of Customer: ')
                while not self.isValid(email):
                    email = input('Enter the valid email of Customer: ')
                query = f"insert into customerDetails values ({max_id},'{name}',{zip},{tax_rate},'{email}');"  
                cursor.execute(query)
                cursor.commit()
                print("\nUser registered successfully\n")
                conn.close()
                exitStatus = input("Enter 1 for User registration menu or other key for main menu: ")
                if exitStatus == '1':
                    self.displayMenu()
                else:
                    commonFunctions.displayMenu()
            except Exception as e:
                print(f'Failed to save customer details with exception: {e}')    

        elif choice == 2:
            try:
                customer_id = int(input('Enter customer ID: '))
                cursor.execute(f'select * from customerDetails where customerID = {customer_id};')
                results = cursor.fetchall()

                x = PrettyTable()

                x.field_names = ["Customer ID", "Name", "ZIP", "Tax Rate", "Email"]
                for result in results:
                    x.add_row(list(result))
                print(x.get_string())
                conn.close()
                self.displayMenu()
            except Exception as e:
                print(f'Failed to fetch customer details with exception: {e}')
        elif choice == 3:
            try:
                cursor.execute(f'select * from customerDetails')
                results = cursor.fetchall()

                x = PrettyTable()

                x.field_names = ["Customer ID", "Name", "ZIP", "Tax Rate", "Email"]
                for result in results:
                    x.add_row(list(result))
                print(x.get_string())
                conn.close()
                self.displayMenu()
            except Exception as e:
                print(f'Failed to fetch customer details with exception: {e}')
        elif choice == 4:
            try:
                customer_id = int(input('Enter customer ID: '))
                cursor.execute(f'delete from customerDetails where customerID = {customer_id};')
                print("Deleted user successfully")
                cursor.commit()
                conn.close()
                self.displayMenu()
            except Exception as e:
                print(f'Failed to fetch customer details with exception: {e}')
        else:
            print('Redirecting to main menu')
            conn.close()
            commonFunctions.displayMenu()

                


    def userDetails(self):
        print("\nUser Registration\n")
        self.displayMenu()


