import database
import config

def get_last_id(table_name):
    connection = database.get_connection()
    id = connection.execute(f"SELECT MAX(id) FROM '{table_name}'").fetchall()
    connection.close()
    return id[0][0] or 0

def fix_value(s):
    return s.replace("\'", "").replace("\"", "")

def fix_db_naming(s):
    return s.lower().replace("\'", "").replace("\"", "").replace(" ", "_")

class StorageItem:
    def __init__(self, category, properties: dict, id_=None):
        self.category = category
        self.table_name = category.get_items_table_name()
        self.properties = properties
        self.id = id_ or get_last_id(self.table_name) + 1

    def save(self):
        connection = database.get_connection()
        id_exists = len(connection.execute(f"SELECT id FROM {self.table_name} WHERE id = {self.id}").fetchall()) > 0
        if id_exists:
            for k in self.properties:
                self.properties[k] = fix_value(self.properties[k])
                if len(self.properties[k]) == 0:
                    self.properties[k] = "~"
            properties = ", ".join(map(lambda key: f"'{fix_db_naming(key)}' = '{fix_value(self.properties[key])}'", self.properties.keys()))
            command = f"UPDATE '{self.table_name}' SET {properties} WHERE id = {self.id}"
            connection.execute(command)
        else:
            if len(self.properties.keys()) > 0:
                keys = "("
                values = "("
                for key in self.properties.keys():
                    keys += fix_db_naming(key) + ", "
                    values += "\'" + fix_value(self.properties[key]) + "\', "
                keys += "id)"
                values += f"{self.id})"
                command = f"INSERT INTO '{self.table_name}' {keys} VALUES {values}"
                connection.execute(command)
            else:  # пустой товар, только id
                command = f"INSERT INTO '{self.table_name}' (id) VALUES ({self.id})"
                connection.execute(command)
        connection.commit()
        connection.close()

    @staticmethod
    def add_property_column(category, parameter_name):
        parameter_name = fix_db_naming(parameter_name)
        connection = database.get_connection()
        connection.execute(f"ALTER TABLE '{category.get_items_table_name()}' ADD {parameter_name} varchar({config.max_property_length}) default '~'")
        connection.commit()
        connection.close()

    @staticmethod
    def select(category, properties : dict):
        connection = database.get_connection()
        conditions = " AND ".join(map(lambda key: f"{fix_db_naming(key)} LIKE '%{fix_value(properties[key])}%'", properties.keys()))
        command = f"SELECT * FROM {category.get_items_table_name()} WHERE {conditions}"
        data = connection.execute(command).fetchall()
        columns = connection.execute(f"PRAGMA table_info({category.get_items_table_name()})").fetchall()
        columns = [c[1].capitalize().replace("_", " ") for c in columns[1:]]  # Все, кроме id
        items_properties = [dict(zip(columns, d[1:])) for d in data]  # Все, кроме id
        res = []
        for i in range(len(data)):
            id_ = data[i][0]
            props = items_properties[i]
            res.append(StorageItem(category, props, id_=id_))
        connection.close()
        return res

    def delete(self):
        connection = database.get_connection()
        connection.execute(f"DELETE FROM {self.table_name} WHERE id = {self.id}")
        connection.commit()
        connection.close()

    @staticmethod
    def does_property_exist(category, property_name):
        connection = database.get_connection()
        columns = connection.execute(f"PRAGMA table_info({category.get_items_table_name()})").fetchall()
        columns = [c[1] for c in columns[1:]]  # Все, кроме id
        property_name = fix_db_naming(property_name)
        connection.close()
        return property_name in columns

    @staticmethod
    def get_properties_and_id_names(category):
        connection = database.get_connection()
        columns = connection.execute(f"PRAGMA table_info({category.get_items_table_name()})").fetchall()
        columns = [c[1].capitalize().replace("_", " ") for c in columns]
        connection.close()
        return columns

    @staticmethod
    def get_all_items_with_ids(category):
        connection = database.get_connection()
        items = connection.execute(f"SELECT * from {category.get_items_table_name()}").fetchall()
        columns = connection.execute(f"PRAGMA table_info({category.get_items_table_name()})").fetchall()
        connection.close()
        columns = [c[1].capitalize().replace("_", " ") for c in columns[1:]]  # Все, кроме id
        items_properties = [dict(zip(columns, d[1:])) for d in items]  # Все, кроме id
        res = []
        for i in range(len(items)):
            id_ = items[i][0]
            props = items_properties[i]
            res.append(StorageItem(category, props, id_=id_))
        return res

    @staticmethod
    def get_by_id(category, id_):
        connection = database.get_connection()
        result = connection.execute(f"SELECT * from {category.get_items_table_name()} WHERE id = {id_}").fetchall()
        if len(result) == 0:
            raise ValueError(f"StorageItem with id {id_} in category {category.name} does not exist")
        else:
            columns = StorageItem.get_properties_and_id_names(category)
            return StorageItem(category, dict(zip(columns[1:], result[0][1:])), id_=result[0][0])

    @staticmethod
    def rename_property(category, old, new):
        old = fix_db_naming(old)
        new = fix_db_naming(new)
        connection = database.get_connection()
        connection.execute(f"ALTER TABLE {category.get_items_table_name()} RENAME COLUMN {old} TO {new}")
        connection.commit()
        connection.close()