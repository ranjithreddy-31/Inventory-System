import pyodbc
from prettytable import PrettyTable


def addItem():
    showItems()
    item_name = input("Choose 1 to add Tv's or choose 2 to add Stereo: ")
    ware_house_number = input("Choose 1 to add in warehouse 1 or choose 2 to add in warehouse 2: ")
    if item_name == '1' and ware_house_number == '1':
        incrementItem(2)
    elif item_name == '2' and ware_house_number == '1':
        incrementItem(1)
    elif item_name == '1' and ware_house_number == '2':
        incrementItem(4)
    elif item_name == '2' and ware_house_number == '2':
        incrementItem(3)
    else:
        print("Incorrect choices please choose again")
        addItem()


def incrementItem(id):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()

    try:
        cur.execute(f"update products set product_quantity = product_quantity + 1 where product_id = {id}")
        print("Product added successfully")
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def showItems():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()

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


def showItemsLessthanFive():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-0BSMBQL\SQLEXPRESS;'
                          'Database=praneeth;'
                          'Trusted_Connection=yes;')
    cur = conn.cursor()

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
    pass


def wareHouse():
    print("Warehouse deails")
    print("1.Add item to inventory")
    print("2.Show product details")
    print("3.Show products less than or equal to 5")
    print("4.Show quantity of each product by warehouse")
    print("Press any other key to exit to main menu")
    ware_house_input = int(input("Enter the number based on the operation that you want to perform: "))
    if ware_house_input == 1:
        addItem()
    elif ware_house_input == 2:
        showItems()
    elif ware_house_input == 3:
        showItemsLessthanFive()
    elif ware_house_input == 4:
        quantityOfItems()
    else:
        # displayMenu()
        pass
