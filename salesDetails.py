import commonFunctions
from datetime import datetime
import pyodbc
from prettytable import PrettyTable
from userDetails import UserDetails
class SalesDetails:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-VU4ECPI;'
                            'Database=praneeth;'
                            'Trusted_Connection=yes;')
        cur = conn.cursor()
        return cur, conn


    def generateInvoice(self):
        customer_id = int(input('Please enter customer ID: '))
        cursor, conn = self.getConnection()

        try:
            cursor.execute(f"select * from customerDetails where customerID = {customer_id};")
            result = cursor.fetchall()

            if not result:
                print('Customer has not registered yet. Please register before generating an invoice')
                userDetails = UserDetails()
                userDetails.displayMenu()
                return
            else:
                item_choice = int(input('Available items \n1. Tv\n2. Stereo\nSelect the item of your choice: '))
                if item_choice == 1:
                    item_name = 'Tv' 
                elif item_choice == 2:
                    item_name = 'Stereos'
                else:
                    print('Choose a valid option')
                    self.salesdisplayMenu()
                    return
                query = f"select product_warehouse,product_quantity from products where product_name = '{item_name}'  and " \
                        f"product_quantity = (select max(product_quantity) from products where product_" \
                        f"name = '{item_name}') "
                cursor.execute(query)
                results = cursor.fetchall()
                warehouse = int(results[0][0])
                product_quantity = int(results[0][1])
                cursor.execute('select max(id) from invoiceDetails')
                res = cursor.fetchall()
                if res:
                    max_id = int(res[0][0]) + 1
                else:
                    max_id = 1
                result = result[0]
                name = result[1]
                zip = int(result[2])
                tax_rate = int(result[3])
                selling_price = int(input('Enter selling price of the item: '))
                delivery_charges = int(input('Enter delivery charges if applicable. Else enter 0: '))
                total_price = selling_price + delivery_charges + ((tax_rate / 100) * selling_price)
                balance = total_price
                date = datetime.today().strftime('%m-%d-%Y')
                query = f"insert into invoiceDetails values ({max_id},'{name}',{zip},{tax_rate},'{item_name}',{selling_price},{delivery_charges},{total_price}, {balance},'{date}',0); "
                cursor.execute(query)
                query = f"update products set product_quantity = {product_quantity - 1} where product_name = '{item_name}' and product_warehouse = {warehouse};"
                cursor.execute(query)
                cursor.commit()
                print('Invoice has been generated successfully')
        except Exception as e:
            print(f'Invoice generating failed with exception: {e}.')
            conn.close()
        finally:
            self.salesdisplayMenu()


    def payInstallment(self):
        invoice_id = int(input('Enter invoice Id: '))

        try:
            cursor, conn = self.getConnection()
            query = f'select id from invoiceDetails where id = {invoice_id};'
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                print('Invalid Invoice ID :(, Please try again')
                self.salesdisplayMenu()
                return
            query = f'select totalPrice,balance,dateOfPurchase from invoiceDetails where id = {invoice_id} and isClosed=0;'
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                print('Invoice is closed !!')
                return
            total_price = result[0][0]
            balance = result[0][1]
            date = result[0][2]
            current_date = datetime.now()
            date = datetime.strptime(date, '%m-%d-%Y')
            days = (current_date - date).days

            if days <= 10:
                print(f'Amount to be paid to close the invoice is: {int(0.9 * int(total_price + balance - total_price))}')
                installment_amount = int(input('Enter installment amount: '))
                balance = int(0.9 * int(total_price + balance - total_price)) - installment_amount
            elif days > 30:
                print(f'Amount to be paid is to close the invoice is: {int(1.02 * int(total_price + balance -  total_price))}')
                installment_amount = int(input('Enter installment amount: '))
                balance = int(1.02 * int(total_price + balance -  total_price)) - installment_amount
            else:
                print(f'Amount to be paid is to close the invoice is: {int(balance)}')
                installment_amount = int(input('Enter installment amount: '))
                balance = int(balance - installment_amount)
            if balance > 0:
                query = f'update invoiceDetails set balance = {balance} where id = {invoice_id};'
                cursor.execute(query)
                cursor.commit()
            else:
                self.closeInvoice(invoice_id, cursor)
            conn.close()
        except Exception as e:
            print(f'Payment process failed with exeption:{e}')
        finally:
            self.salesdisplayMenu()


    def closeInvoice(self,invoice_id=None, cursor = None):
        if not invoice_id:
            if not cursor:
                cursor, conn = self.getConnection()
            invoice_id = int(input('Enter invoice Id: '))
            query = f'select id from invoiceDetails where id = {invoice_id} and isClosed=0;'
            cursor.execute(query)
            result = cursor.fetchall()
            if not result[0][0]:
                print('Invalid Invoice ID :(, Please try again')
                self.salesdisplayMenu()
                return
        else:
            invoice_id = invoice_id
        try:
            cursor, connection = self.getConnection()
            query = f'update invoiceDetails set isClosed = 1, balance = 0 where id = {invoice_id};'
            cursor.execute(query)
            cursor.commit()
            connection.close()
            print(f'Invoice: {invoice_id} has been closed successfully!!')
        except Exception as e:
            print(f'Failed closing invoice with exception: {e}')
        finally:
            self.salesdisplayMenu()


    def showOpenInvoices(self):
        try:
            cursor, connection = self.getConnection()
            query = f'select * from invoiceDetails where isClosed=0 order by dateOfPurchase;'
            cursor.execute(query)
            results = cursor.fetchall()

            x = PrettyTable()

            x.field_names = ["Invoice ID", "Name", "ZIP", "Tax Rate", "Item", "Selling Price", "Delivery Charge", "Total Cost",
                            "Amount to be paid", "Date of Purchase", "Is Invoice closed"]
            for result in results:
                x.add_row(list(result))
            print(x.get_string())
            connection.close()
        except Exception as e:
            print(f'Failed fetching invoices with exception: {e}')
        finally:
            self.salesdisplayMenu()


    def showClosedInvoices(self):
        try:
            cursor, connection = self.getConnection()
            query = f'select * from invoiceDetails where isClosed =1 order by totalPrice desc;'
            cursor.execute(query)
            results = cursor.fetchall()
            x = PrettyTable()
            x.field_names = ["Invoice ID", "Name", "ZIP", "Tax Rate", "Item", "Selling Price", "Delivery Charge",
                            "Total Cost", "Amount to be paid", "Date of Purchase", "Is Invoice closed"]
            for result in results:
                x.add_row(list(result))
            print(x.get_string())
            connection.close()
        except Exception as e:
            print(f'Failed fetching invoices with exception: {e}')
        finally:
            self.salesdisplayMenu()


    def salesdisplayMenu(self):
        print()
        print()
        print('1. Generate an invoice')
        print('2. Pay an installment')
        print('3. Show open invoices')
        print('4. Show closed invoices')
        print('5. Quit')
        print()
        print()
        option = int(input('Select an option from the above menu: '))

        if option == 1:
            self.generateInvoice()
        elif option == 2:
            self.payInstallment()
        elif option == 3:
            self.showOpenInvoices()
        elif option == 4:
            self.showClosedInvoices()
        else:
            return commonFunctions.displayMenu()
        return "exit"


    def salesDetails(self):
        print('\nWelcome to Sales and Invoices module.')
        self.salesdisplayMenu()



