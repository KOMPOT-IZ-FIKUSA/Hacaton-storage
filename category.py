import database

def get_last_category_id():
    connection = database.get_connection()
    id = connection.execute("SELECT MAX(id) FROM categories").fetchall()
    connection.close()
    return id[0][0] or 0

def fix_db_naming(s):
    return s.lower().replace("\'", "").replace("\"", "").replace(" ", "_")

class Category:
    def __init__(self, name: str, id_=None):
        self.__name = name
        self.__db_name = fix_db_naming(name)
        self.id = id_ or get_last_category_id() + 1

    def get_name(self):
        return self.__name

    def get_db_name(self):
        return self.__db_name

    def set_name(self, name):
        self.__name = name
        self.__db_name = fix_db_naming(name)

    def save(self):
        connection = database.get_connection()
        connection.execute(f"CREATE TABLE IF NOT EXISTS {self.get_items_table_name()} (id INTEGER PRIMARY KEY)")
        id_exists = len(connection.execute(f"SELECT id FROM categories WHERE id = {self.id}").fetchall()) > 0
        if id_exists:
            connection.execute(f"UPDATE categories SET name = '{self.__db_name}' WHERE id = {self.id}")
        else:
            connection.execute(f"INSERT INTO categories VALUES ({self.id}, '{self.__db_name}')")
            connection.commit()
        connection.close()


    def delete(self):
        connection = database.get_connection()
        connection.execute(f"DELETE FROM categories WHERE id = {self.id}")

        i = 0
        while True:
            try:
                connection.execute(f"ALTER TABLE {self.get_items_table_name()} RENAME TO {self.get_items_table_name() + f'_deleted_{i}'}")
            except:
                i += 1
                continue
            break

        connection.commit()
        connection.close()


    @staticmethod
    def get_by_name(name):
        connection = database.get_connection()
        res = connection.execute(f"SELECT id FROM categories WHERE name = '{fix_db_naming(name)}'").fetchall()
        connection.close()
        if len(res) == 0:
            raise ValueError(f"Name '{name}' does not exist in table 'categories'")
        return Category(name, res[0][0])

    @staticmethod
    def get_by_id(id_):
        connection = database.get_connection()
        res = connection.execute(f"SELECT name FROM categories WHERE id = '{id_}'").fetchall()
        if len(res) == 0:
            raise ValueError(f"Id '{id_}' does not exist in table 'categories'")
        return Category(res[0][0].replace("_", " ").capitalize(), id_)

    def __str__(self):
        return f"Категория[{self.__name}]"

    def get_items_table_name(self):
        return self.__db_name


    @staticmethod
    def get_all_categories():
        connection = database.get_connection()
        res = connection.execute("SELECT * FROM categories").fetchall()
        res = [Category(t[1].replace("_", " ").capitalize(), id_=t[0]) for t in res]
        connection.close()
        return res

    @staticmethod
    def does_name_exist(name):
        connection = database.get_connection()
        res = connection.execute(f"SELECT * FROM categories WHERE name = '{fix_db_naming(name)}'").fetchall()
        return len(res) > 0

    @staticmethod
    def rename(old, new):
        old = fix_db_naming(old)
        new = fix_db_naming(new)
        connection = database.get_connection()
        connection.execute(f"UPDATE categories SET name = '{new}' WHERE name = '{old}'")
        connection.execute(f"ALTER TABLE {old} RENAME TO {new}")
        connection.commit()
        connection.close()