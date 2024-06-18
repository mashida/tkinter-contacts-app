from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tk_message_box

root = Tk()
root.title("Список контактов")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(False, False)
root.config(bg="#6666ff")

# ============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()


# ============================METHODS=====================================

def database_setup():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, "
        "lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()


def submit_data():
    if (FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or
            CONTACT.get() == ""):
        tk_message_box.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (
                str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()),
                str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")


def update_data():
    if GENDER.get() == "":
        tk_message_box.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `age` = ?,  `address` = ?, `contact` = "
            "? WHERE `mem_id` = ?",
            (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(AGE.get()), str(ADDRESS.get()),
             str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()


def on_selected(event: Event = None):
    global mem_id, UpdateWindow
    cur_item = tree.focus()
    contents = (tree.item(cur_item))
    selected_item = contents['values']
    mem_id = selected_item[0]
    FIRSTNAME.set(selected_item[1])
    LASTNAME.set(selected_item[2])
    GENDER.set(selected_item[3])
    AGE.set(selected_item[4])
    ADDRESS.set(selected_item[5])
    CONTACT.set(selected_item[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2) + 450) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    UpdateWindow.resizable(False, False)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    # ===================FRAMES==============================
    form_title = Frame(UpdateWindow)
    form_title.pack(side=TOP)
    contact_form = Frame(UpdateWindow)
    contact_form.pack(side=TOP, pady=10)
    radio_group = Frame(contact_form)
    Radiobutton(radio_group, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(radio_group, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    # ===================LABELS==============================
    lbl_title = Label(form_title, text="Обновление контактов", font=('arial', 16), bg="orange", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(contact_form, text="Имя", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(contact_form, text="Фамилия", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(contact_form, text="Пол", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(contact_form, text="Возраст", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(contact_form, text="Адрес", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(contact_form, text="Контакт", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    # ===================ENTRY===============================
    firstname = Entry(contact_form, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(contact_form, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    radio_group.grid(row=2, column=1)
    age = Entry(contact_form, textvariable=AGE, font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(contact_form, textvariable=ADDRESS, font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(contact_form, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=5, column=1)

    # ==================BUTTONS==============================
    btn_update_con = Button(contact_form, text="Update", width=50, command=update_data)
    btn_update_con.grid(row=6, columnspan=2, pady=10)


def delete_data():
    if not tree.selection():
        tk_message_box.showwarning('', 'Сначала выберите что-нибудь!', icon="warning")
    else:
        result = tk_message_box.askquestion('', 'Вы уверены, что хотите удалить эту запись?', icon="warning")
        if result == 'yes':
            cur_item = tree.focus()
            contents = (tree.item(cur_item))
            selected_item = contents['values']
            tree.delete(cur_item)
            conn = sqlite3.connect("contacts.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selected_item[0])
            conn.commit()
            cursor.close()
            conn.close()


def add_new_contact_window():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("Male")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Список контактов")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2) - 455) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    NewWindow.resizable(False, False)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    # ===================FRAMES==============================
    form_title = Frame(NewWindow)
    form_title.pack(side=TOP)
    contact_form = Frame(NewWindow)
    contact_form.pack(side=TOP, pady=10)
    radio_group = Frame(contact_form)
    Radiobutton(radio_group, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(radio_group, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    # ===================LABELS==============================
    lbl_title = Label(form_title, text="Adding New Contacts", font=('arial', 16), bg="#66ff66", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(contact_form, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(contact_form, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(contact_form, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(contact_form, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(contact_form, text="Address", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(contact_form, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    # ===================ENTRY===============================
    firstname = Entry(contact_form, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(contact_form, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    radio_group.grid(row=2, column=1)
    age = Entry(contact_form, textvariable=AGE, font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(contact_form, textvariable=ADDRESS, font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(contact_form, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=5, column=1)

    # ==================BUTTONS==============================
    btn_add_con = Button(contact_form, text="Save", width=50, command=submit_data)
    btn_add_con.grid(row=6, columnspan=2, pady=10)


# ============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#6666ff")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
# ============================LABELS======================================
lbl_title = Label(Top, text="Система управления контактами", font=('arial', 16), width=500)
lbl_title.pack(fill=X)

# ============================ENTRY=======================================

# ============================BUTTONS=====================================
btn_add = Button(MidLeft, text="+ ADD NEW", bg="#66ff66", command=add_new_contact_window)
btn_add.pack()
btn_delete = Button(MidRight, text="DELETE", bg="red", command=delete_data)
btn_delete.pack(side=RIGHT)

# ============================TABLES======================================
scroll_bar_x = Scrollbar(TableMargin, orient=HORIZONTAL)
scroll_bar_y = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
                    height=400, selectmode="extended", yscrollcommand=scroll_bar_y.set, xscrollcommand=scroll_bar_x.set)
scroll_bar_y.config(command=tree.yview)
scroll_bar_y.pack(side=RIGHT, fill=Y)
scroll_bar_x.config(command=tree.xview)
scroll_bar_x.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', on_selected)

# ============================INITIALIZATION==============================
if __name__ == '__main__':
    database_setup()
    root.mainloop()
