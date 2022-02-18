import commonFunctions
import pyodbc
from prettytable import PrettyTable

def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn

def displayMenu():
    choice = int(input('1. Add new Customer\n2. Get Customer Details\n3. Delete Customer Details\n4. Quit \nChoose '
                       'an option: '))
    cursor, conn = getConnection()
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

            query = f"insert into customerDetails values ({max_id},'{name}',{zip},{tax_rate},'{email}');"  
            cursor.execute(query)
            cursor.commit()
            print("\n User registered successfully")
            conn.close()
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
            displayMenu()
        except Exception as e:
            print(f'Failed to fetch customer details with exception: {e}')
    elif choice == 3:
        try:
            customer_id = int(input('Enter customer ID: '))
            cursor.execute(f'delete from customerDetails where customerID = {customer_id};')
            print("Deleted user successfully")
            cursor.commit()
            conn.close()
            displayMenu()
        except Exception as e:
            print(f'Failed to fetch customer details with exception: {e}')
    else:
        conn.close()
        commonFunctions.displayMenu()

            


def userDetails():
    print("\nUser Registration\n")
    displayMenu()


