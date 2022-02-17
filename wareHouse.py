from commonFunctions import *
import pyodbc
from prettytable import PrettyTable


def getConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()
    return cur, conn


def addItem():
    showItems()
    item_name = input("Choose 1 to add Tv's or choose 2 to add Stereo: ")
    ware_house_number = input("Choose 1 to add in warehouse 1 or choose 2 to add in warehouse 2: ")
    if item_name == '1' and ware_house_number == '1':
        confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \n If you are sure press 1 to "
                             f"confirm or other key to choose again")
        if confirmation == '1':
            incrementItem(2)
        else:
            addItem()
    elif item_name == '2' and ware_house_number == '1':
        confirmation = input(f"You are adding Stereos in warehouse {ware_house_number}. \n If you are sure press 1 to "
                             f"confirm or other key to choose again")
        if confirmation == '1':
            incrementItem(1)
        else:
            addItem()
    elif item_name == '1' and ware_house_number == '2':
        confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \n If you are sure press 1 to "
                             f"confirm or other key to choose again")
        if confirmation == '1':
            incrementItem(4)
        else:
            addItem()
    elif item_name == '2' and ware_house_number == '2':
        confirmation = input(f"You are adding Stereos in warehouse {ware_house_number}. \n If you are sure press 1 to "
                             f"confirm or other key to choose again")
        if confirmation == '1':
            incrementItem(3)
        else:
            addItem()
    else:
        print("Incorrect choices please choose again")
        addItem()
    wareHouse()


def incrementItem(id):
    cur, conn = getConnection()

    try:
        quantity = int(input("Enter the number of items: "))
        cur.execute(f"update products set product_quantity = product_quantity + {quantity} where product_id = {id}")
        print("Products added successfully")
        wareHouse()
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def showItems():
    cur, conn = getConnection()
    try:
        cur.execute("select * from products")
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
    wareHouse()


def showItemsLessthanFive():
    cur, conn = getConnection()

    try:
        cur.execute("select  product_name, sum(product_quantity) as total_quantity from products group by "
                    "product_name having sum(product_quantity) <= 5 order by sum(product_quantity)")
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


def quantityOfItems():
    showItems()


def wareHouse():
    print()
    print()
    print("Warehouse deails")
    print("1.Add item to inventory")
    print("2.Show product details")
    print("3.Show products less than or equal to 5")
    print("4.Show quantity of each product by warehouse")
    print("Press any other key to exit to main menu")
    print()
    print()
    ware_house_input = input("Enter the number based on the operation that you want to perform: ")
    if ware_house_input == '1':
        addItem()
    elif ware_house_input == '2':
        showItems()
    elif ware_house_input == '3':
        showItemsLessthanFive()
    elif ware_house_input == '4':
        quantityOfItems()
    else:
        displayMenu()
