import pyodbc

def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn

def displayMenu():
    choice = int(input('Choose an option:\n 1. SqlScriptsAdd new Customer\n 2. Get Customer Details\n 3. Delete Customer Details'))
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
            zip = int(input('Enter the ZIP de of customer: '))
            tax_rate = int(input('Enter the tax percentage: '))
            email = input('Enter the email of Customer: ')

            query = f"insert into customerDetails values ({max_id},'{name}',{zip},{tax_rate},'{email}');"  
            cursor.execute(query)
            cursor.commit()
        except Exception as e:
            print(f'Failed to save customer details with exception: {e}')    

    elif choice == 2:
        try:
            customer_id = int(input('Enter customer ID: '))
            cursor.execute(f'select * from customerDetails where customerID = {customer_id};')
            results = cursor.fetchall()
            print(results[0])
        except Exception as e:
            print(f'Failed to fetch customer details with exception: {e}')    
    else:
        try:
            customer_id = int(input('Enter customer ID: '))
            cursor.execute(f'delete from customerDetails where customerID = {customer_id};')
            cursor.commit()
        except Exception as e:
            print(f'Failed to fetch customer details with exception: {e}')  
    conn.close()
            


def userDetails():
    print("User Registration")
    displayMenu()


