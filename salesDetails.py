from datetime import datetime
import pyodbc 
from prettytable import PrettyTable
def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-VU4ECPI;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    return conn

def generateInvoice():
    customer_id = int(input('Please enter customer ID: '))
    connection = getConnection()
    cursor = connection.cursor()

    try: 
        cursor.execute(f"select * from customerDetails where customerID = {customer_id};")
        result = cursor.fetchall()[0]
        
        if not result:
            print('Customer has not registered yet. Please register before generating an invice')
            return
        else:
            cursor.execute('select max(id) from invoiceDetails')
            res = cursor.fetchall()[0]
            if res[0]:
                max_id = int(res[0])+1
            else:
                max_id = 1
            print(result)
            name = result[1]
            zip = int(result[2])
            tax_rate = int(result[3])
            item_name = input('Enter the name of the item purchased: ')
            selling_price = int(input('Enter selling price of the item: '))
            delivery_charges = int(input('Enter delivery charges if applicable. Else enter 0: '))
            total_price = selling_price+delivery_charges+((tax_rate/100)*selling_price)
            date = datetime.today().strftime('%m-%d-%Y')
            query = f"insert into invoiceDetails values ({max_id},'{name}',{zip},{tax_rate},'{item_name}',{selling_price},{delivery_charges},{total_price}, '{date}',0); "

            cursor.execute(query)
            cursor.commit()
            print('Invoice has been generated successfully')
    except Exception as e:
        print(f'Invoice generating failed with exception: {e}.')
        connection.close()

def payInstallment():
    invoice_id = int(input('Enter invoice Id: '))
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = f'select totalPrice,dateOfPurchase from invoiceDetails where id = {invoice_id};'
        cursor.execute(query)
        result = cursor.fetchall()
        total_price = result[0][0]
        date = result[0][1]
        installment_amount = int(input('Enter installment amount: '))
        current_date = datetime.now()
        date = datetime.strptime(date, '%m-%d-%Y')
        days = (current_date - date).days
    
        if days<=10:
            balance = (0.9 * int(total_price)) - installment_amount
        elif days>30:
            balance = (1.02 * int(total_price)) - installment_amount
        else:
            balance = total_price - installment_amount
        if balance>0:
            query = f'update invoiceDetails set totalPrice = {balance} where id = {invoice_id};'
            cursor.execute(query)
            cursor.commit()
        else:
            closeInvoice(invoice_id)
        connection.close()
    except Exception as e:
        print(f'Payment process failed with exeption:{e}')

def closeInvoice(invoice_id = None):
    if not invoice_id:
        invoice_id = int(input('Enter invoice Id: '))
    else:
        invoice_id = invoice_id
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = f'update invoiceDetails set isClosed = 1 where id = {invoice_id};'
        cursor.execute(query)
        cursor.commit()
        connection.close()
    except Exception as e:
        print(f'Failed closing invoice with exception: {e}')

def showOpenInvoices():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = f'select * from invoiceDetails where isClosed=0 order by dateOfPurchase;'
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
        connection.close()
    except Exception as e:
        print(f'Failed fetching invoices with exception: {e}')

def showClosedInvoices():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = f'select * from invoiceDetails where isClosed =1 order by totalPrice desc;'
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result) 
        connection.close()
    except Exception as e:
        print(f'Failed fetching invoices with exception: {e}')
            
def displayMenu():
    print('Welcome to Sales and Invoices module.')
    print('1. Generate an invoice')
    print('2. Pay an installment')
    print('3. Show open invoices')
    print('4. Show closed invoices')
    print('5. Quit')
    
    option = int(input('Select an option from the above menu: '))
    
    if option == 1:
        generateInvoice()
    elif option == 2:
        payInstallment()
    elif option == 3:
        showOpenInvoices()
    elif option == 4:
        showClosedInvoices()
    else:
        return "exit"
    return "exit"


def salesDetails():
    print("Sales and Invoices")
    displayMenu()
salesDetails()