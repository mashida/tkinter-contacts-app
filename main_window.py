import tkinter.ttk as ttk
import tkinter.messagebox as tk_message_box
from sqlite3 import Connection
from tkinter import Tk, StringVar, Frame, SOLID, TOP, LEFT, RIGHT, Label, X, Button, Scrollbar, HORIZONTAL, VERTICAL, Y, \
    BOTTOM, W, NO, Event, Toplevel, Radiobutton, Entry
from typing import Optional

from database import data_insert, data_fetch, database_update, data_delete


class MainWindow:
    def __init__(self, conn: Connection):
        self.root = Tk()
        self.conn = conn
        # variables
        self.firstname = StringVar()
        self.surname = StringVar()
        self.gender = StringVar()
        self.age = StringVar()
        self.address = StringVar()
        self.contact = StringVar()
        self.mem_id = ""
        # frames
        self.top = Frame(self.root, width=500, bd=0, relief=SOLID, bg="#094391")
        self.top.pack(side=TOP)
        self.mid = Frame(self.root, width=500, bg="#094391")
        self.mid.pack(side=TOP)
        self.mid_left = Frame(self.mid, width=0)
        self.mid_left.pack(side=LEFT, pady=5)
        self.mid_left_padding = Frame(self.mid, width=420, bg="#094391")
        self.mid_left_padding.pack(side=LEFT)
        self.mid_right = Frame(self.mid, width=100)
        self.mid_right.pack(side=RIGHT, pady=5)
        self.table_margin = Frame(self.root, width=500)
        self.table_margin.pack(side=TOP)
        # labels
        # self.lbl_title = Label(self.top, text="Система управления контактами", font=('arial', 16), width=500)
        # self.lbl_title.pack(fill=X)
        # buttons
        self.btn_add = Button(self.mid_left, text="Добавить контакт", bg="#BECBFE", command=self.on_add_new_contact)
        self.btn_add.pack()
        self.btn_delete = Button(self.mid_right, text="Удалить контакт", bg="#BECBFE", command=self.on_delete)
        self.btn_delete.pack(side=RIGHT)

        # tables
        self.scroll_bar_x = Scrollbar(self.table_margin, orient=HORIZONTAL)
        self.scroll_bar_y = Scrollbar(self.table_margin, orient=VERTICAL)
        self.tree = ttk.Treeview(self.table_margin,
                                 columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
                                 height=400, selectmode="extended", yscrollcommand=self.scroll_bar_y.set,
                                 xscrollcommand=self.scroll_bar_x.set)
        self.scroll_bar_y.config(command=self.tree.yview)
        self.scroll_bar_y.pack(side=RIGHT, fill=Y)
        self.scroll_bar_x.config(command=self.tree.xview)
        self.scroll_bar_x.pack(side=BOTTOM, fill=X)

        # Windows
        self.new_window: Optional[Toplevel] = None

        # setup
        self.setup_main_window()
        self.setup_tree()

    def setup_tree(self):
        self.tree.heading('MemberID', text="MemberID", anchor=W)
        self.tree.heading('Firstname', text="Имя", anchor=W)
        self.tree.heading('Lastname', text="Фамилия", anchor=W)
        self.tree.heading('Gender', text="Пол", anchor=W)
        self.tree.heading('Age', text="Возраст", anchor=W)
        self.tree.heading('Address', text="Адрес", anchor=W)
        self.tree.heading('Contact', text="Контакт", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#2', stretch=NO, minwidth=0, width=80)
        self.tree.column('#3', stretch=NO, minwidth=0, width=120)
        self.tree.column('#4', stretch=NO, minwidth=0, width=90)
        self.tree.column('#5', stretch=NO, minwidth=0, width=80)
        self.tree.column('#6', stretch=NO, minwidth=0, width=120)
        self.tree.column('#7', stretch=NO, minwidth=0, width=120)
        self.tree.pack()
        self.tree.bind('<Double-Button-1>', self.on_select_row)

    def setup_main_window(self):
        self.root.title("Список контактов")
        width = 700
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.root.resizable(False, False)
        self.root.config(bg="#094391")

    def on_add_new_contact(self):
        self.firstname.set("")
        self.surname.set("")
        self.gender.set("М")
        self.age.set("")
        self.address.set("")
        self.contact.set("")
        self.new_window = Toplevel()
        self.new_window.title("Добавить контакт | Список контактов")
        # self.new_window.bind("Return", self.on_submit())
        width = 336
        height = 260
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = ((screen_width / 2) - 455) - (width / 2)
        y = ((screen_height / 2) + 20) - (height / 2)
        self.new_window.resizable(False, False)
        self.new_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        if 'UpdateWindow' in globals():
            UpdateWindow.destroy()

        form_title = Frame(self.new_window)
        form_title.pack(side=TOP)
        contact_form = Frame(self.new_window)
        contact_form.pack(side=TOP, pady=10)
        radio_group = Frame(contact_form)
        Radiobutton(radio_group, text="М", variable=self.gender, value="М", font=('arial', 14)).pack(side=LEFT)
        Radiobutton(radio_group, text="Ж", variable=self.gender, value="Ж", font=('arial', 14)).pack(
            side=LEFT)

        # lbl_title = Label(form_title, text="Adding New Contacts", font=('arial', 16), bg="#66ff66", width=300)
        # lbl_title.pack(fill=X)
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

        firstname = Entry(contact_form, textvariable=self.firstname, font=('arial', 14))
        firstname.grid(row=0, column=1)
        lastname = Entry(contact_form, textvariable=self.surname, font=('arial', 14))
        lastname.grid(row=1, column=1)
        radio_group.grid(row=2, column=1)
        age = Entry(contact_form, textvariable=self.age, font=('arial', 14))
        age.grid(row=3, column=1)
        address = Entry(contact_form, textvariable=self.address, font=('arial', 14))
        address.grid(row=4, column=1)
        contact = Entry(contact_form, textvariable=self.contact, font=('arial', 14))
        contact.grid(row=5, column=1)

        btn_add_con = Button(contact_form, text="Сохранить", width=44, command=self.on_submit)
        btn_add_con.grid(row=6, columnspan=2, pady=10)

    def on_submit(self, event: Event = None):
        if (self.firstname.get() == "" or self.surname.get() == "" or self.gender.get() == "" or
                self.age.get() == "" or self.address.get() == "" or self.contact.get() == ""):
            tk_message_box.showwarning('', 'Пожалуйста заполните требуемое поле', icon="warning")
        else:
            self.tree.delete(*self.tree.get_children())
            data_insert(self.conn, [str(self.firstname.get()), str(self.surname.get()), str(self.gender.get()),
                                    int(self.age.get()), str(self.address.get()), str(self.contact.get())])

            data_fetch(self.conn, self.tree)
            self.set_all_values_empty()

    def set_all_values_empty(self):
        self.firstname.set("")
        self.surname.set("")
        self.gender.set("М")
        self.age.set("")
        self.address.set("")
        self.contact.set("")

    def on_update_data(self, event: Event = None):
        if self.gender.get() == "":
            tk_message_box.showwarning('', 'Пожалуйста заполните требуемое поле', icon="warning")
        else:
            self.tree.delete(*self.tree.get_children())
            database_update(conn=self.conn,
                            values=[str(self.firstname.get()), str(self.surname.get()), str(self.gender.get()),
                                    str(self.age.get()), str(self.address.get()), str(self.contact.get()),
                                    int(self.mem_id)])
            data_fetch(conn=self.conn, tree=self.tree)

    def on_select_row(self, event: Event = None):
        global UpdateWindow
        cur_item = self.tree.focus()
        contents = (self.tree.item(cur_item))
        selected_item = contents['values']
        self.mem_id = selected_item[0]
        self.firstname.set(selected_item[1])
        self.surname.set(selected_item[2])
        self.gender.set(selected_item[3])
        self.age.set(selected_item[4])
        self.address.set(selected_item[5])
        self.contact.set(selected_item[6])
        UpdateWindow = Toplevel()
        UpdateWindow.title("Обновить контакт | Список контактов")
        width = 336
        height = 260
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = ((screen_width / 2) + 450) - (width / 2)
        y = ((screen_height / 2) + 20) - (height / 2)
        UpdateWindow.resizable(False, False)
        UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
        if 'NewWindow' in globals():
            self.new_window.destroy()

        # frames
        form_title = Frame(UpdateWindow)
        form_title.pack(side=TOP)
        contact_form = Frame(UpdateWindow)
        contact_form.pack(side=TOP, pady=10)
        radio_group = Frame(contact_form)
        Radiobutton(radio_group, text="М", variable=self.gender, value="М", font=('arial', 14)).pack(side=LEFT)
        Radiobutton(radio_group, text="Ж", variable=self.gender, value="Ж", font=('arial', 14)).pack(
            side=LEFT)

        # labels
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

        # entry
        firstname = Entry(contact_form, textvariable=self.firstname, font=('arial', 14))
        firstname.grid(row=0, column=1)
        lastname = Entry(contact_form, textvariable=self.surname, font=('arial', 14))
        lastname.grid(row=1, column=1)
        radio_group.grid(row=2, column=1)
        age = Entry(contact_form, textvariable=self.age, font=('arial', 14))
        age.grid(row=3, column=1)
        address = Entry(contact_form, textvariable=self.address, font=('arial', 14))
        address.grid(row=4, column=1)
        contact = Entry(contact_form, textvariable=self.contact, font=('arial', 14))
        contact.grid(row=5, column=1)

        # buttons
        btn_update_con = Button(contact_form, text="Обновить", width=44, command=self.on_update_data)
        btn_update_con.grid(row=6, columnspan=2, pady=10)

    def on_delete(self, event: Event = None):
        if not self.tree.selection():
            tk_message_box.showwarning('', 'Сначала выберите что-нибудь!', icon="warning")
        else:
            result = tk_message_box.askquestion('', 'Вы уверены, что хотите удалить эту запись?', icon="warning")
            if result == 'yes':
                cur_item = self.tree.focus()
                contents = (self.tree.item(cur_item))
                selected_item = contents['values']
                self.tree.delete(*self.tree.get_children())
                data_delete(conn=self.conn, value=selected_item[0])
                data_fetch(conn=self.conn, tree=self.tree)
