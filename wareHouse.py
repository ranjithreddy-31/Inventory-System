import commonFunctions
import pyodbc
from prettytable import PrettyTable

class WareHouse:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=DESKTOP-VU4ECPI;'
                            'Database=praneeth;'
                            'Trusted_Connection=yes;')
        cur = conn.cursor()
        return cur, conn


    def addItem(self):
        item_name = input("\nChoose 1 to add Tv's or choose 2 to add Stereo: ")
        ware_house_number = input("Choose 1 to add in warehouse 1 or choose 2 to add in warehouse 2: ")
        print()
        if item_name == '1' and ware_house_number == '1':
            confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(2)
            else:
                self.addItem()
        elif item_name == '2' and ware_house_number == '1':
            confirmation = input(f"You are adding Stereos in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(1)
            else:
                self.addItem()
        elif item_name == '1' and ware_house_number == '2':
            confirmation = input(f"You are adding Tv's in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(4)
            else:
                self.addItem()
        elif item_name == '2' and ware_house_number == '2':
            confirmation = input(f"You are adding Stereos in warehouse {ware_house_number}. \nIf you are sure press 1 to "
                                f"confirm or other key to choose again: ")
            if confirmation == '1':
                self.incrementItem(3)
            else:
                self.addItem()
        else:
            print("Incorrect choices please choose again")
            self.addItem()
        self.wareHouse()


    def incrementItem(self, id):
        cur, conn = self.getConnection()

        try:
            quantity = int(input("Enter the number of items: "))
            cur.execute(f"update products set product_quantity = product_quantity + {quantity} where product_id = {id}")
            print("Products added successfully")
        except Exception as e:
            print(e)
        conn.commit()
        conn.close()


    def showItems(self):
        cur, conn = self.getConnection()
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
        self.wareHouse()


    def showItemsLessthanFive(self):
        cur, conn = self.getConnection()

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
        self.wareHouse()


    def quantityOfItems(self):
        self.showItems()


    def wareHouse(self):
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
            self.addItem()
        elif ware_house_input == '2':
            self.showItems()
        elif ware_house_input == '3':
            self.showItemsLessthanFive()
        elif ware_house_input == '4':
            self.quantityOfItems()
        else:
            commonFunctions.displayMenu()
