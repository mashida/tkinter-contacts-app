from sqlite3 import Connection


def database_setup(conn: Connection):
    """
    Create database if it does not exist
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, "
        "lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")

    cursor.close()


def data_fetch(conn: Connection, tree):
    """
    fetch all data from database and save it to ttk.TreeView
    :param conn: sqlite3 connection
    :param tree: ttk.TreeView object
    :return: None
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)


def data_insert(conn: Connection, values: list[str | int]) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", values)
    conn.commit()


def database_update(conn: Connection, values: list[str | int]) -> None:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `age` = ?,  `address` = ?, "
        "`contact` = ? WHERE `mem_id` = ?", values)
    conn.commit()


def data_delete(conn: Connection, value: str | int) -> None:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % value)
    conn.commit()
