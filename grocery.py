from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk


root = Tk()
root.title('Supermarket Management')
root.geometry("1000x600")
root.resizable(False, False)
# root.wm_iconbitmap('logo.ico')

TabControl = ttk.Notebook(root)
tab1 = ttk.Frame(TabControl)
tab2 = ttk.Frame(TabControl)
tab3 = ttk.Frame(TabControl)
TabControl.add(tab1, text = "Available Items")
TabControl.add(tab2, text = "Purchased Items")
TabControl.add(tab3, text = "About Software")
TabControl.pack(fill = "both", expand = 1)

database = 'Inventory.db'
Pdatabase = 'Purchased.db'
def query_database():
	for record in my_tree.get_children():
		my_tree.delete(record)
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("SELECT rowid, * FROM inventory")
	records = c.fetchall()
	global count
	count = 0
	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6]), tags=('oddrow',))
		count += 1

	conn.commit()
	conn.close()

def search_records():
	#Clarify this code
	if selected_tab == tab1:
		db = "inventory"
		tree = my_tree
	else:
		db = "Purchased"
		tree = Purchased_tree
	
	lookup_record = search_entry.get()
	search_for = searchVar.get()
	search_frame.destroy()
	for record in tree.get_children():
		my_tree.delete(record)
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute(f"SELECT rowid, * FROM {db} WHERE {search_for} like ?", (lookup_record,))
	records = c.fetchall()
	global count
	count = 0
	for record in records:
		if count % 2 == 0:
			tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6]), tags=('evenrow',))
		else:
			tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6]), tags=('oddrow',))
		count += 1
	conn.commit()
	conn.close()

def lookup_records():
	global search_entry, search_frame, searchVar
	search_frame = LabelFrame(tab1, text="Barcode")
	search_frame.place(x = 20, y=2)
	search_entry = Entry(search_frame, font=("Helvetica", 18))
	search_entry.pack(pady=15, padx=15)

	searchVar = StringVar()
	search_combo = ttk.Combobox(search_frame, textvariable = searchVar, width = 20, state = 'readonly')
	search_combo['values'] = ['Item', 'Barcode', 'SerialNum', 'Units', 'Date_']

	search_combo.set('--Search for--')
	search_combo.pack(padx = 10, pady = 10)

	search_button = Button(search_frame, text="Search Records", command=search_records)
	search_button.pack(padx = 10, pady = 10)
	exit_button = Button(search_frame, text = "Exit", command = lambda :[search_frame.destroy()])
	exit_button.pack(padx = 10, pady = 10)

def primary_color():
	primary_color = colorchooser.askcolor()[1]
	if primary_color:
		my_tree.tag_configure('evenrow', background=primary_color)

def secondary_color():
	secondary_color = colorchooser.askcolor()[1]
	if secondary_color:
		my_tree.tag_configure('oddrow', background=secondary_color)

def highlight_color():
	highlight_color = colorchooser.askcolor()[1]
	if highlight_color:
		style.map('Treeview',
			background=[('selected', highlight_color)])
		
my_menu = Menu(root)
root.config(menu=my_menu)

option_menu =  Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

conn = sqlite3.connect(database)
c = conn.cursor()

c.execute("""CREATE TABLE if not exists inventory (
	Item text,
	Barcode int,
	SerialNum int,
	Units text,
	Price text,
	Date_ text)
	""")

conn.commit()
conn.close()

connect = sqlite3.connect(Pdatabase)
cursor = connect.cursor()

cursor.execute("""CREATE TABLE if not exists Purchased (
	Item text,
	Barcode int,
	SerialNum int,
	Units text,
	Price text,
	Date_ text,
	Customer text)
	""")

connect.commit()
connect.close()

style = ttk.Style()
# print(style.theme_names())
style.theme_use('xpnative')

style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

style.map('Treeview',
	background=[('selected', "green")])

tree_frame = Frame(tab1)
tree_frame.pack(pady=10, expand = False)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()
tree_scroll.config(command=my_tree.yview)
my_tree['columns'] = ("Item", "Barcode", "S/N", "Qty/Units", "Price", "Date")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item", anchor=W, width=230)
my_tree.column("Barcode", anchor=W, width=100)
my_tree.column("S/N", anchor=CENTER, width=70)
my_tree.column("Qty/Units", anchor=CENTER, width=140)
my_tree.column("Price", anchor=CENTER, width=140)
my_tree.column("Date", anchor=CENTER, width=140)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Item", text="Item", anchor=W)
my_tree.heading("Barcode", text="Barcode", anchor=W)
my_tree.heading("S/N", text="S No.", anchor=CENTER)
my_tree.heading("Qty/Units", text="Qty/Units", anchor=CENTER)
my_tree.heading("Price", text="Price", anchor=CENTER)
my_tree.heading("Date", text="Date", anchor=CENTER)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

data_frame = LabelFrame(tab1, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

Item_label = Label(data_frame, text="Item")
Item_label.grid(row=0, column=0, padx=10, pady=10)
Item_entry = Entry(data_frame)
Item_entry.grid(row=0, column=1, padx=10, pady=10)

Barcode_label = Label(data_frame, text="Barcode")
Barcode_label.grid(row=0, column=2, padx=10, pady=10)
Barcode_entry = Entry(data_frame)
Barcode_entry.grid(row=0, column=3, padx=10, pady=10)

serial_label = Label(data_frame, text="S No.")
serial_label.grid(row=0, column=4, padx=10, pady=10)
serial_entry = Entry(data_frame)
serial_entry.grid(row=0, column=5, padx=10, pady=10)

units_label = Label(data_frame, text="Qty/Units")
units_label.grid(row=1, column=0, padx=10, pady=10)
units_entry = Entry(data_frame)
units_entry.grid(row=1, column=1, padx=10, pady=10)

price_label = Label(data_frame, text="Price")
price_label.grid(row=1, column=2, padx=10, pady=10)
price_entry = Entry(data_frame)
price_entry.grid(row=1, column=3, padx=10, pady=10)

Date_label = Label(data_frame, text="Date")
Date_label.grid(row=1, column=4, padx=10, pady=10)
Date_entry = Entry(data_frame)
Date_entry.grid(row=1, column=5, padx=10, pady=10)


Ptree_frame = Frame(tab2)
Ptree_frame.pack(pady=10, expand = False)
Ptree_scroll = Scrollbar(Ptree_frame)
Ptree_scroll.pack(side=RIGHT, fill=Y)
Purchased_tree = ttk.Treeview(Ptree_frame, yscrollcommand=Ptree_scroll.set, selectmode="extended")
Purchased_tree.pack()
Ptree_scroll.config(command=Purchased_tree.yview)
Purchased_tree['columns'] = ("Item", "Barcode", "S/N", "Qty/Units", "Price", "Date", "Customer")

Purchased_tree.column("#0", width=0, stretch=NO)
Purchased_tree.column("Item", anchor=W, width=230)
Purchased_tree.column("Barcode", anchor=W, width=100)
Purchased_tree.column("S/N", anchor=CENTER, width=70)
Purchased_tree.column("Qty/Units", anchor=CENTER, width=140)
Purchased_tree.column("Price", anchor=CENTER, width=140)
Purchased_tree.column("Date", anchor=CENTER, width=140)
Purchased_tree.column("Customer", anchor=CENTER, width=100)

Purchased_tree.heading("#0", text="", anchor=W)
Purchased_tree.heading("Item", text="Item", anchor=W)
Purchased_tree.heading("Barcode", text="Barcode", anchor=W)
Purchased_tree.heading("S/N", text="S No.", anchor=CENTER)
Purchased_tree.heading("Qty/Units", text="Qty/Units", anchor=CENTER)
Purchased_tree.heading("Price", text="Price", anchor=CENTER)
Purchased_tree.heading("Date", text="Date", anchor=CENTER)
Purchased_tree.heading("Customer", text = "Customer", anchor=CENTER)

Purchased_tree.tag_configure('oddrow', background="white")
Purchased_tree.tag_configure('evenrow', background="lightblue")

Pdata_frame = LabelFrame(tab2, text="Record")
Pdata_frame.pack(fill="x", expand="yes", padx=20)

PItem_label = Label(Pdata_frame, text="Item")
PItem_label.grid(row=0, column=0, padx=10, pady=10)
PItem_entry = Entry(Pdata_frame)
PItem_entry.grid(row=0, column=1, padx=10, pady=10)

PBarcode_label = Label(Pdata_frame, text="Barcode")
PBarcode_label.grid(row=0, column=2, padx=10, pady=10)
PBarcode_entry = Entry(Pdata_frame)
PBarcode_entry.grid(row=0, column=3, padx=10, pady=10)

Pserial_label = Label(Pdata_frame, text="S/N")
Pserial_label.grid(row=0, column=4, padx=10, pady=10)
Pserial_entry = Entry(Pdata_frame)
Pserial_entry.grid(row=0, column=5, padx=10, pady=10)

Punits_label = Label(Pdata_frame, text="Qty/Units")
Punits_label.grid(row=1, column=0, padx=10, pady=10)
Punits_entry = Entry(Pdata_frame)
Punits_entry.grid(row=1, column=1, padx=10, pady=10)

Pprice_label = Label(Pdata_frame, text="Price")
Pprice_label.grid(row=1, column=2, padx=10, pady=10)
Pprice_entry = Entry(Pdata_frame)
Pprice_entry.grid(row=1, column=3, padx=10, pady=10)

PDate_label = Label(Pdata_frame, text="Date")
PDate_label.grid(row=1, column=4, padx=10, pady=10)
PDate_entry = Entry(Pdata_frame)
PDate_entry.grid(row=1, column=5, padx=10, pady=10)

Customer_label = Label(Pdata_frame, text="Customer")
Customer_label.grid(row=1, column=6, padx=10, pady=10)
Customer_entry = Entry(Pdata_frame)
Customer_entry.grid(row=1, column=7, padx=10, pady=10)

def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

def remove_one():
	x = my_tree.selection()[0]
	my_tree.delete(x)
	# values = my_tree.item(x, 'values')
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("DELETE from inventory WHERE oid =" + serial_entry.get())
	# Item_entry.insert(0, values[0])
	
	conn.commit()
	conn.close()
	clear_entries()
	messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

def remove_many():
	response = messagebox.askyesno("Warning!", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	if response == 1:
		x = my_tree.selection()
		ids_to_delete = []
		
		for record in x:
			ids_to_delete.append(my_tree.item(record, 'values')[2])
		for record in x:
			my_tree.delete(record)
		conn = sqlite3.connect(database)
		c = conn.cursor()
		
		c.executemany("DELETE FROM inventory WHERE SerialNum = ?", [(a,) for a in ids_to_delete])
		ids_to_delete = []

		conn.commit()
		conn.close()
		clear_entries()


def remove_all():
	response = messagebox.askyesno("Warning!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")
	if response == 1:
		for record in my_tree.get_children():
			my_tree.delete(record)
		conn = sqlite3.connect(database)
		c = conn.cursor()
		c.execute("DROP TABLE inventory")

		conn.commit()
		conn.close()
		clear_entries()
		create_table_again()

def clear_entries():
	serial_entry.delete(0, END)
	Barcode_entry.delete(0, END)
	Item_entry.delete(0, END)
	units_entry.delete(0, END)
	price_entry.delete(0, END)
	Date_entry.delete(0, END)

def select_record(e):
	serial_entry.delete(0, END)
	Barcode_entry.delete(0, END)
	Item_entry.delete(0, END)
	units_entry.delete(0, END)
	price_entry.delete(0, END)
	Date_entry.delete(0, END)

	selected = my_tree.focus()
	values = my_tree.item(selected, 'values')

	Item_entry.insert(0, values[0])
	Barcode_entry.insert(0, values[1])
	serial_entry.insert(0, values[2])
	units_entry.insert(0, values[3])
	price_entry.insert(0, values[4])
	Date_entry.insert(0, values[5])

def update_record():
	selected = my_tree.focus()
	my_tree.item(selected, text="",
		values=(Item_entry.get(), Barcode_entry.get(), serial_entry.get(), units_entry.get(), price_entry.get(), Date_entry.get(),))
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute("""UPDATE inventory SET
		Item = :Item,
		Barcode = :barcode,
		SerialNum = :serial_num,
		Units = :Units,
		Price = :Price,
		Date_ = :Date_
		""",
		{
			'Item': Item_entry.get(),
			'barcode': Barcode_entry.get(),
			'serial_num': serial_entry.get(),
			'Units':units_entry.get(),
			'Price': price_entry.get(),
			'Date_': Date_entry.get(),
		})

	conn.commit()
	conn.close()
	serial_entry.delete(0, END)
	Barcode_entry.delete(0, END)
	Item_entry.delete(0, END)
	units_entry.delete(0, END)
	price_entry.delete(0, END)
	Date_entry.delete(0, END)

def add_record():
	conn = sqlite3.connect(database)

	c = conn.cursor()
	c.execute("INSERT INTO inventory VALUES (:Item, :barcode, :serial_num, :Units, :Price, :Date_)",
		{
			'Item': Item_entry.get(),
			'barcode': Barcode_entry.get(),
			'serial_num': serial_entry.get(),
			'Units': units_entry.get(),
			'Price': price_entry.get(),
			'Date_': Date_entry.get()
		})
	
	conn.commit()
	conn.close()

	serial_entry.delete(0, END)
	Barcode_entry.delete(0, END)
	Item_entry.delete(0, END)
	units_entry.delete(0, END)
	price_entry.delete(0, END)
	Date_entry.delete(0, END)

	my_tree.delete(*my_tree.get_children())

	query_database()

def create_table_again():
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""CREATE TABLE if not exists inventory (
		Item text,
		Barcode int,
		SerialNum int,
		Units text,
		Price text,
		Date_ text)
		""")

	conn.commit()
	conn.close()

def PurchaseItem():
	values = my_tree.item(my_tree.focus(), 'values')
	try:

		Pserial_entry.delete(0, END)
		PBarcode_entry.delete(0, END)
		PItem_entry.delete(0, END)
		Punits_entry.delete(0, END)
		Pprice_entry.delete(0, END)
		PDate_entry.delete(0, END)

		PItem_entry.insert(0, values[0])
		PBarcode_entry.insert(0, values[1])
		Pserial_entry.insert(0, values[2])
		# Punits_entry.insert(0, values[3])
		Pprice_entry.insert(0, values[4])
		PDate_entry.insert(0, values[5])
	except:
		pass

	Purchased.Purchase_query_database()
	TabControl.select(tab2)


class Purchased:
	def Purchase_query_database():
		for record in Purchased_tree.get_children():
			Purchased_tree.delete(record)
		connect = sqlite3.connect(Pdatabase)
		cursor = connect.cursor()
		cursor.execute("SELECT rowid, * FROM Purchased")
		records = cursor.fetchall()
		global count
		count = 0
		for record in records:
			if count % 2 == 0:
				Purchased_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]), tags=('evenrow',))
			else:
				Purchased_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]), tags=('oddrow',))
			count += 1

		connect.commit()
		connect.close()

	def primary_color():
		primary_color = colorchooser.askcolor()[1]
		if primary_color:
			Purchased_tree.tag_configure('evenrow', background=primary_color)

	def secondary_color():
		secondary_color = colorchooser.askcolor()[1]
		if secondary_color:
			Purchased_tree.tag_configure('oddrow', background=secondary_color)

	def highlight_color():
		highlight_color = colorchooser.askcolor()[1]
		if highlight_color:
			style.map('Treeview',
				background=[('selected', highlight_color)])

	connect = sqlite3.connect(Pdatabase)
	cursor = connect.cursor()

	cursor.execute("""CREATE TABLE if not exists Purchased (
		Item text,
		Barcode int,
		SerialNum int,
		Units text,
		Price text,
		Date_ text,
		Customer text)
		""")

	connect.commit()
	connect.close()

	def up():
		rows = Purchased_tree.selection()
		for row in rows:
			Purchased_tree.move(row, Purchased_tree.parent(row), Purchased_tree.index(row)-1)

	def down():
		rows = Purchased_tree.selection()
		for row in reversed(rows):
			Purchased_tree.move(row, Purchased_tree.parent(row), Purchased_tree.index(row)+1)

	def remove_one():
		x = Purchased_tree.selection()[0]
		Purchased_tree.delete(x)
		connect = sqlite3.connect(Pdatabase)
		cursor = connect.cursor()
		cursor.execute("DELETE from Purchased WHERE oid=" + Pserial_entry.get())
	
		connect.commit()
		connect.close()
		clear_entries()
		messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

	def remove_many():
		response = messagebox.askyesno("Warning!", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

		if response == 1:
			x = Purchased_tree.selection()
			ids_to_delete = []
		
			for record in x:
				ids_to_delete.append(Purchased_tree.item(record, 'values')[2])
			for record in x:
				Purchased_tree.delete(record)
			connect = sqlite3.connect(Pdatabase)
			cursor = connect.cursor()
		
			cursor.executemany("DELETE FROM Purchased WHERE id = ?", [a for a in ids_to_delete])
			ids_to_delete = []

			connect.commit()
			connect.close()
			clear_entries()


	def remove_all():
		response = messagebox.askyesno("Warning!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")
		if response == 1:
			for record in Purchased_tree.get_children():
				Purchased_tree.delete(record)
			connect = sqlite3.connect(Pdatabase)
			cursor = connect.cursor()
			cursor.execute("DROP TABLE Purchased")

			connect.commit()
			connect.close()
			clear_entries()
			create_table_again()

	def clear_entries():
		Pserial_entry.delete(0, END)
		PBarcode_entry.delete(0, END)
		PItem_entry.delete(0, END)
		Punits_entry.delete(0, END)
		Pprice_entry.delete(0, END)
		PDate_entry.delete(0, END)
		Customer_entry.delete(0, END)


	def select_record(e):
		Pserial_entry.delete(0, END)
		PBarcode_entry.delete(0, END)
		PItem_entry.delete(0, END)
		Punits_entry.delete(0, END)
		Pprice_entry.delete(0, END)
		PDate_entry.delete(0, END)
		Customer_entry.delete(0, END)

		selected = Purchased_tree.focus()
		values = Purchased_tree.item(selected, 'values')

		Pserial_entry.insert(0, values[0])
		PBarcode_entry.insert(0, values[1])
		PItem_entry.insert(0, values[2])
		Punits_entry.insert(0, values[3])
		Pprice_entry.insert(0, values[4])
		PDate_entry.insert(0, values[5])
		Customer_entry.insert(0, values[6])

	def update_record():
		selected = Purchased_tree.focus()
		Purchased_tree.item(selected, text="", values=(Pserial_entry.get(), PBarcode_entry.get(), PItem_entry.get(), Punits_entry.get(), Pprice_entry.get(), PDate_entry.get(), Customer_entry.get(),))
		connect = sqlite3.connect(Pdatabase)
		cursor = connect.cursor()
		cursor.execute("""UPDATE Purchased SET
			Item = :Item,
			Barcode = :barcode,
			SerialNum = :serial_num,
			Units = :Units,
			Price = :Price,
			Date_ = :Date_,
			Customer = :Customer,
			WHERE oid = :oid""",
			{
				'Item':PItem_entry.get(),
				'barcode': PBarcode_entry.get(),
				'serial_num': Pserial_entry.get(),
				'Units':Punits_entry.get(),
				'Price': Pprice_entry.get(),
				'Date_': PDate_entry.get(),
				'Customer':Customer_entry.get()
			})

		connect.commit()
		connect.close()
		Pserial_entry.delete(0, END)
		PBarcode_entry.delete(0, END)
		PItem_entry.delete(0, END)
		Punits_entry.delete(0, END)
		Pprice_entry.delete(0, END)
		PDate_entry.delete(0, END)
		Customer_entry.delete(0, END)

	def add_record():
		Purchased.create_table_again()
		connect = sqlite3.connect(Pdatabase)
		cursor = connect.cursor()
		cursor.execute("INSERT INTO Purchased VALUES (:Item, :barcode, :serial_num, :Units, :Price, :Date_, :Customer)",
			{
				'Item':PItem_entry.get(),
				'barcode': PBarcode_entry.get(),
				'serial_num': Pserial_entry.get(),
				'Units': Punits_entry.get(),
				'Price': Pprice_entry.get(),
				'Date_': PDate_entry.get(),
				'Customer':Customer_entry.get(),
			})

		connect.commit()
		connect.close()

		Pserial_entry.delete(0, END)
		PBarcode_entry.delete(0, END)
		PItem_entry.delete(0, END)
		# Punits_entry.delete(0, END)
		Pprice_entry.delete(0, END)
		PDate_entry.delete(0, END)
		Customer_entry.delete(0, END)

		Purchased_tree.delete(*Purchased_tree.get_children())

		# values = my_tree.item(my_tree.focus(), 'values')
		# units_ = Punits_entry.get()
		# newUnits = int(values[3]) - int(units_)
		# try:
		# 	serial_entry.delete(0, END)
		# 	Barcode_entry.delete(0, END)
		# 	Item_entry.delete(0, END)
		# 	units_entry.delete(0, END)
		# 	price_entry.delete(0, END)
		# 	Date_entry.delete(0, END)
			
		# 	price_entry.delete(0, END)
		# 	price_entry.insert(0, newUnits)
		# 	update_record()
		# except Exception as e:
		# 	messagebox.showerror("Error", e)

		Purchased.Purchase_query_database()

	def create_table_again():
		connect = sqlite3.connect(Pdatabase)
		cursor = connect.cursor()
		cursor.execute("""CREATE TABLE if not exists Purchased (
			Item text,
			Barcode int,
			SerialNum int,
			Units text,
			Price text,
			Date_ text,
			Customer text)
			""")
		connect.commit()
		connect.close()


Pbutton_frame = LabelFrame(tab2, text="Commands")
Pbutton_frame.pack()

Pupdate_button = Button(Pbutton_frame, text="Update Record", command=Purchased.update_record)
Pupdate_button.grid(row=0, column=0, padx=10, pady=10)

Padd_button = Button(Pbutton_frame, text="Add Record", command=Purchased.add_record)
Padd_button.grid(row=0, column=1, padx=10, pady=10)


Premove_all_button = Button(Pbutton_frame, text="Clear Records", command=Purchased.remove_all)
Premove_all_button.grid(row=0, column=2, padx=10, pady=10)

Premove_one_button = Button(Pbutton_frame, text="Remove Selected", command=Purchased.remove_one)
Premove_one_button.grid(row=0, column=3, padx=10, pady=10)

Premove_many_button = Button(Pbutton_frame, text="Remove All Selected", command=Purchased.remove_many)
Premove_many_button.grid(row=0, column=4, padx=10, pady=10)

Pmove_up_button = Button(Pbutton_frame, text="Move Up", command=up)
Pmove_up_button.grid(row=0, column=5, padx=10, pady=10)

Pmove_down_button = Button(Pbutton_frame, text="Move Down", command=down)
Pmove_down_button.grid(row=0, column=6, padx=10, pady=10)

Pselect_record_button = Button(Pbutton_frame, text="Clear Entry Boxes", command=clear_entries)
Pselect_record_button.grid(row=0, column=7, padx=10, pady=10)

Purchased_tree.bind("<Button-1>", select_record)
Purchased_tree.bind("DELETE", remove_one)
Purchased.Purchase_query_database()


button_frame = LabelFrame(tab1, text="Commands")
button_frame.pack()

update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Clear Records", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)


remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
remove_one_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="Move Up", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="Move Down", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

purchase_button = Button(button_frame, text = "Purchase Item", command = PurchaseItem)
purchase_button.grid(row = 0, column = 8, padx = 10, pady = 10)

my_tree.bind("<Button-1>", select_record)
my_tree.bind("DELETE", remove_one)
query_database()


About = """ This Software is a beta test grocery software management software that
was created by Praise James as a demo to Tasahil Pos. It can be used to enter an
inventory of grocery store records (tracking the items in the store) while tracking
the purchase history as well with a secure and only admin privileged rights for use

Let it be known that this version of this software is NOT FOR SALE, as it is only
to be tested and is not allowed for commercial use or distribution until the 
commercial version is released by the programmer of this software.

(c) Copyright Praise James
"""

About_label = Label(tab3, text = About, font=("Helvetica", 17))
About_label.pack()
root.mainloop()
