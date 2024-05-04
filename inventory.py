from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="veenus@2003",
    database="inventory_system"
)

mycursor = conn.cursor()

class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="ADD NEW PRODUCT", font=('arial 40 bold'), fg='green',bg='grey')
        self.heading.place(x=450, y=0)

        # labels for the window
        self.name_l = Label(master, text="Whats the product", font=('Calibri 20 bold'))
        self.name_l.place(x=0, y=100)

        self.stock_l = Label(master, text="What are the stocks", font=('Calibri 20 bold'))
        self.stock_l.place(x=0, y=180)

        self.cp_l = Label(master, text="Please enter the price ", font=('Calibri 20 bold'))
        self.cp_l.place(x=0, y=260)

        # entries for window
        self.name_e = Entry(master, width=25, font=('Calibri 20 bold'))
        self.name_e.place(x=380, y=100)

        self.stock_e = Entry(master, width=25, font=('Calibri 20 bold'))
        self.stock_e.place(x=380, y=180)

        self.cp_e = Entry(master, width=25, font=('Calibri 20 bold'))
        self.cp_e.place(x=380, y=260)

        # button to add to the database
        self.btn_add = Button(master, text='Update the database', width=30, height=3, bg='Lightgreen', fg='Black',
                              command=self.get_items, font=2)
        self.btn_add.place(x=800, y=100)

        self.btn_clear = Button(master, text="Reset the fields", width=30, height=3, bg='red', fg='Black',
                                command=self.clear_all, font=2)
        self.btn_clear.place(x=800, y=180)

        # text box for the log
        self.tbBox = Text(master, width=50, height=10)
        self.tbBox.place(x=50, y=420)

        # Initialize ID number
        self.id = 1

        # Set up event bindings
        self.master.bind('<Return>', self.get_items)
        self.master.bind('<Up>', self.clear_all)

    def get_items(self, event=None):
        # get from entries
        self.name = self.name_e.get()
        self.stock = self.stock_e.get()
        self.cp = self.cp_e.get()

        # dynamic entries
        if self.name == '' or self.stock == '' or self.cp == '':
            messagebox.showinfo("Error", "Please Fill all the entries.")
        else:
            mycursor.execute("INSERT INTO inventory(name, stock, price) VALUES(%s,%s,%s)",
                             [self.name, self.stock, self.cp])
            conn.commit()
            # textbox insert
            self.tbBox.insert(END, "\n\nInserted " + str(self.name) + " into the database with the quantity of " + str(
                self.stock))
            messagebox.showinfo("Success", "Successfully added to the database")

    def clear_all(self, event=None):
        num = self.id + 1
        self.name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.cp_e.delete(0, END)

class Application():
    products_list = []
    product_price = []
    product_quantity = []
    product_id = []

    def __init__(self, master, *args, **kwargs):
        self.master = master

        # Left Frame
        self.left = Frame(master, width=750, height=768, bg='grey')
        self.left.pack(side=LEFT)

        # Right Frame
        self.right = Frame(master, width=500, height=500, bg='white')
        self.right.pack(side=RIGHT)

        # Labels and Entry Widgets
        self.heading = Label(self.left, text="H&M ", font=('ALGERIAN 40 bold'), fg='red',bg='grey')
        self.heading.place(x=500, y=10)

        self.date_l = Label(self.right, text="Date: ", font=('Calibri 18 bold'), fg='black')
        self.date_l.place(x=140, y=0)

        self.tproduct = Label(self.right, text="Products", font=('Calibri 20 bold'), fg='Black')
        self.tproduct.place(x=0, y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('Calibri 20 bold'), fg='Black')
        self.tquantity.place(x=150, y=60)

        self.tamount = Label(self.right, text="Price", font=('Calibri 20 bold'), fg='Black')
        self.tamount.place(x=300, y=60)

        self.enterid = Label(self.left, text="ID Number", font=('calibri 20 bold'), fg='black')
        self.enterid.place(x=50, y=80)

        self.enteride = Entry(self.left, width=25, font=('Calibri 18 bold'), bg='white')
        self.enteride.place(x=220, y=80)
        self.enteride.focus()

        self.search_btn = Button(self.left, text="Find", width=18, height=2, bg='white', command=self.ajax)
        self.search_btn.place(x=580, y=70)

        self.productname = Label(self.left, text="Name", font=('ALGERIAN 27 bold'), bg='white', fg='black')
        self.productname.place(x=50, y=200)

        self.pprice = Label(self.left, text="price", font=('ALGERIAN 27 bold'), bg='white', fg='black')
        self.pprice.place(x=50, y=250)

        self.total_l = Label(self.right, text="total", font=('arial 40 bold'), bg='grey', fg='white')
        self.total_l.place(x=0, y=400)

        # Button to switch to Window Two
        self.switch_btn = Button(self.left, text="ADD NEW PRODUCT",font=('arial 10 bold'), width=25, height=2, bg='white', fg='black', command=self.switch_to_window_two)
        self.switch_btn.place(x=350, y=550)

    def switch_to_window_two(self):
        # Destroy the current window and create an instance of Window Two
        self.master.destroy()
        window_two_root = Tk()
        window_two_app = WindowTwo(window_two_root)
        window_two_root.mainloop()

    def ajax(self, *args, **kwargs):
        try:
            self.conn = mysql.connector.connect(host='localhost', database='inventory_system', user='root', password='veenus@2003')
            self.mycursor = self.conn.cursor()
            get_id = self.enteride.get()
            self.mycursor.execute("SELECT * FROM inventory WHERE id= %s", [get_id])
            self.pc = self.mycursor.fetchall()

            if self.pc:
                for r in self.pc:
                    self.get_id = r[0]
                    self.get_name = r[1]
                    self.get_price = r[3]
                    self.get_stock = r[2]

                # Update the displayed product's name
                self.productname.configure(text="Product's Name: " + str(self.get_name), fg='black', bg='white',
                                           font=('calibri,20,bold'))
                self.productname.place(x=50, y=200)

                self.quantityl = Label(self.left, text="Enter the qty ", font=('Calibri 18 bold'), fg='black',
                                       bg='white')
                self.quantityl.place(x=0, y=300)

                self.quantity_e = Entry(self.left, width=10, font=('Calibri 18 bold'), bg='white')
                self.quantity_e.place(x=170, y=300)
                self.quantity_e.focus()

                self.discount_l = Label(self.left, text="Discount ", font=('Calibri 20 bold'), fg='black',
                                        bg='white')
                self.discount_l.place(x=320, y=300)

                self.discount_e = Entry(self.left, text="bill reciept",width=10, font=('Calibri 20 bold'), fg='black', bg='white')
                self.discount_e.place(x=430, y=300)
                self.discount_e.insert(END, 0)

                self.add_to_cart_btn = Button(self.left, text="Display on the bill receipt", width=18, height=3,
                                              bg='purple',fg='white', command=self.add_to_cart)
                self.add_to_cart_btn.place(x=200, y=370)

                self.change_l = Label(self.left, text="Enter the amount paid", font=('Calibri 20 bold'), fg='black',
                                      bg='white')
                self.change_l.place(x=0, y=450)

                self.change_e = Entry(self.left, width=10, font=('Calibri 18 bold'), bg='white')
                self.change_e.place(x=280, y=450)

                self.change_btn = Button(self.left, text="Calculate the difference", width=22, height=2, bg='purple',fg='white',
                                          command=self.change_func)
                self.change_btn.place(x=430, y=450)

                self.bill_btn = Button(self.left, text="Create a bill of the items purchased", width=30, height=2,
                                       bg='Purple', fg='white', command=self.generate_bill)
                self.bill_btn.place(x=0, y=550)
            else:
                messagebox.showinfo("Product Not Found", f"No product found with ID {get_id}")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            if self.conn.is_connected():
                self.mycursor.close()
                self.conn.close()

    def add_to_cart(self, *args, **kwargs):
        try:
            # Ensure these variables are defined before using them
            self.quantity_value = int(self.quantity_e.get())
            if self.quantity_value > int(self.get_stock):
                messagebox.showinfo("Error", "Not enough products in our stock.")
            else:
                # calculate the price first
                self.final_price = (float(self.quantity_value) * float(self.get_price)) - (float(self.discount_e.get()))
                Application.products_list.append(self.get_name)
                Application.product_price.append(self.final_price)
                Application.product_quantity.append(self.quantity_value)
                Application.product_id.append(self.get_id)

                self.x_index = 0
                self.y_index = 100
                self.counter = 0
                for self.p in Application.products_list:
                    self.tempname = Label(self.right, text=str(Application.products_list[self.counter]), font=('arial 18 bold'),
                                          bg='gray', fg='white')
                    self.tempname.place(x=0, y=self.y_index)
                    self.tempqt = Label(self.right, text=str(Application.product_quantity[self.counter]), font=('arial 18 bold'),
                                        bg='gray', fg='white')
                    self.tempqt.place(x=150, y=self.y_index)
                    self.tempprice = Label(self.right, text=str(Application.product_price[self.counter]), font=('arial 18 bold'),
                                           bg='gray', fg='white')
                    self.tempprice.place(x=300, y=self.y_index)

                    self.y_index += 40
                    self.counter += 1

                # total configure
                self.total_l.configure(text="Final amount=Rs. " + str(sum(Application.product_price)), bg='gray', fg='white',
                                       font=('20'))
                self.total_l.place(x=180, y=450)
                # delete
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.add_to_cart_btn.destroy()
                # autofocus to the enter id
                self.enteride.focus()
                self.quantityl.focus()
                self.enteride.delete(0, END)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity.")

    def change_func(self, *args, **kwargs):
        self.amount_given = float(self.change_e.get())
        self.our_total = float(sum(Application.product_price))

        self.to_give = self.amount_given - self.our_total

        # label change
        self.c_amount = Label(self.left, text="Change is Rs. " + str(self.to_give), font=('Calibri 20 bold'),
                              fg='Black', bg='white')
        self.c_amount.place(x=0, y=500)

    def generate_bill(self, *args, **kwargs):
        try:
            # Reconnect and create a new cursor
            self.conn = mysql.connector.connect(host='localhost', database='inventory_system', user='root',
                                                password='veenus@2003')
            self.mycursor = self.conn.cursor()

            for i, product in enumerate(Application.products_list):
                for r in self.pc:
                    self.old_stock = r[2]
                    if i < len(Application.product_quantity):
                        self.new_stock = int(self.old_stock) - int(Application.product_quantity[i])
                        # updating the stock
                        self.mycursor.execute("UPDATE inventory SET stock=%s WHERE id=%s",
                                              [self.new_stock, self.get_id])
                        self.conn.commit()

                        # insert into transaction
                        self.mycursor.execute(
                            "INSERT INTO transacion (product_name, quantity, amount, date,inven_id) VALUES(%s, %s, %s, %s,%s)",
                            [self.get_name, Application.product_quantity[i], self.get_price, datetime.now(),self.get_id])
                        self.conn.commit()
                        print("Decreased")
                        self.mycursor.execute(
                            "INSERT INTO item (name, purchase_id) VALUES(%s, %s)",
                            [self.get_name, self.get_id])
                        self.conn.commit()
                        print("Decreased")
                        self.mycursor.execute(
                            "INSERT INTO ordered_inventory (name,purchased_no) VALUES(%s, %s)",
                            [self.get_name,Application.product_quantity[i]])
                        self.conn.commit()
                        print("Decreased")

            messagebox.showinfo("Successfully Done", "Transaction completed successfully.")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            # Close the cursor and connection in the finally block to ensure it's always closed
            if self.mycursor:
                self.mycursor.close()
            if self.conn.is_connected():
                self.conn.close()

class WindowTwo():
    def __init__(self, master, *args, **kwargs):
        self.master = master

        # Left Frame
        self.left = Frame(master, width=750, height=768, bg='grey')
        self.left.pack(side=LEFT)

        # Right Frame
        self.right = Frame(master, width=750, height=768, bg='grey')
        self.right.pack(side=RIGHT)

        # Labels and Entry Widgets
        self.heading = Label(self.left, text=" ", font=('ALGERIAN 30 bold'), bg='grey')
        self.heading.place(x=100, y=10)

        # Add more widgets for Window Two as needed...
        self.db_window = Database(master)
        #self.switch_btn = Button(self.left, text="NEW ", width=25, height=2, bg='purple', fg='white',
                                 #command=self.switch_to_window_two)
    def switch_to_database_window(self):
        # Show the Database window
        self.db_window.master.deiconify()
        # Hide the current window
        self.master.withdraw()
if __name__ == "__main__":
    # Create Tkinter root window

    root = Tk()
    app = Application(root)
    root.mainloop()
