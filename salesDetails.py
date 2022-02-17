from datetime import datetime
import pyodbc 
from prettytable import PrettyTable

def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn

def generateInvoice():
    customer_id = int(input('Please enter customer ID: '))
    cursor, conn = getConnection()

    try: 
        cursor.execute(f"select * from customerDetails where customerID = {customer_id};")
        result = cursor.fetchall()[0]
        
        if not result:
            print('Customer has not registered yet. Please register before generating an invice')
            return
        else:
            item_choice = int(input('Select the item of you choice:\n1. Tv\n2. Stereo'))
            item_name = 'Tv' if item_choice == 1 else 'Stereos'
            query = f"select product_warehouse,product_quantity from products where product_name = '{item_name}'  and product_quantity = (select max(product_quantity) from products where product_name = '{item_name}')"
            cursor.execute(query)
            results = cursor.fetchall()
            warehouse  = int(results[0][0])
            product_quantity = int(results[0][1])
            cursor.execute('select max(id) from invoiceDetails')
            res = cursor.fetchall()[0]
            if res[0]:
                max_id = int(res[0])+1
            else:
                max_id = 1
            name = result[1]
            zip = int(result[2])
            tax_rate = int(result[3])
            selling_price = int(input('Enter selling price of the item: '))
            delivery_charges = int(input('Enter delivery charges if applicable. Else enter 0: '))
            total_price = selling_price+delivery_charges+((tax_rate/100)*selling_price)
            date = datetime.today().strftime('%m-%d-%Y')
            query = f"insert into invoiceDetails values ({max_id},'{name}',{zip},{tax_rate},'{item_name}',{selling_price},{delivery_charges},{total_price}, '{date}',0); "
            cursor.execute(query)
            query = f"update products set product_quantity = {product_quantity-1} where product_name = '{item_name}' and product_warehouse = {warehouse};"
            cursor.execute(query)
            cursor.commit()
            print('Invoice has been generated successfully')
    except Exception as e:
        print(f'Invoice generating failed with exception: {e}.')
        conn.close()
    finally:
        displayMenu()


def payInstallment():
    invoice_id = int(input('Enter invoice Id: '))
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = f'select totalPrice,dateOfPurchase from invoiceDetails where id = {invoice_id} and isClosed=0;'
        cursor.execute(query)
        result = cursor.fetchall()
        if not result[0][0]:
            print('Invoice is closed !!')
            return
        total_price = result[0][0]
        date = result[0][1]
        current_date = datetime.now()
        date = datetime.strptime(date, '%m-%d-%Y')
        days = (current_date - date).days
    
        if days<=10:
            print(f'Amount to be paid to close the invoice is: {int(0.9 * int(total_price))}')
            installment_amount = int(input('Enter installment amount: '))
            balance = int(0.9 * int(total_price)) - installment_amount
        elif days>30:
            print(f'Amount to be paid is to close the invoice is: {int(1.02 * int(total_price))}')
            installment_amount = int(input('Enter installment amount: '))
            balance = int(1.02 * int(total_price)) - installment_amount
        else:
            print(f'Amount to be paid is to close the invoice is: {int(total_price)}')
            installment_amount = int(input('Enter installment amount: '))
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
    finally:
        displayMenu()

def closeInvoice(invoice_id = None):
    if not invoice_id:
        invoice_id = int(input('Enter invoice Id: '))
    else:
        invoice_id = invoice_id
    try:
        cursor, connection = getConnection()
        query = f'update invoiceDetails set isClosed = 1 where id = {invoice_id};'
        cursor.execute(query)
        cursor.commit()
        connection.close()
        print(f'Invoice: {invoice_id} has been closed successfully!!')
    except Exception as e:
        print(f'Failed closing invoice with exception: {e}')
    finally:
        displayMenu()

def showOpenInvoices():
    try:
        cursor, connection = getConnection()
        query = f'select * from invoiceDetails where isClosed=0 order by dateOfPurchase;'
        cursor.execute(query)
        results = cursor.fetchall()

        x = PrettyTable()

        x.field_names = ["Invoice ID", "Name", "ZIP", "Tax Rate", "Item", "Selling Price", "Delivery Charge", "Amount to be paid", "Date of Purchase", "Is Invoice closed"]
        for result in results:
            x.add_row(list(result))
        print(x.get_string())
        connection.close()
    except Exception as e:
        print(f'Failed fetching invoices with exception: {e}')
    finally:
        displayMenu()

def showClosedInvoices():
    try:
        cursor, connection = getConnection()
        query = f'select * from invoiceDetails where isClosed =1 order by totalPrice desc;'
        cursor.execute(query)
        results = cursor.fetchall()
        x = PrettyTable()
        x.field_names = ["Invoice ID", "Name", "ZIP", "Tax Rate", "Item", "Selling Price", "Delivery Charge", "Total Cost", "Date of Purchase", "Is Invoice closed"]
        for result in results:
            x.add_row(list(result))
        print(x.get_string())
        connection.close()
    except Exception as e:
        print(f'Failed fetching invoices with exception: {e}')
    finally:
        displayMenu()
def displayMenu():
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
    print('Welcome to Sales and Invoices module.')
    displayMenu()
