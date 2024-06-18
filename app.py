import sqlite3

from main_window import MainWindow
from database import data_fetch, database_setup

if __name__ == '__main__':
    with sqlite3.connect("contacts1.db") as conn:
        database_setup(conn)
        app = MainWindow(conn=conn)
        data_fetch(conn=conn, tree=app.tree)
        app.root.mainloop()
