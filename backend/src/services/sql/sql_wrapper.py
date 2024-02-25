import sqlite3


class SQLmanager:

    def __init__(self, db):
        self.conn = sqlite3.connect(f'{db}')
        self.cursor = self.conn.cursor()

    def insert_row(self, table_name: str, data: dict):

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())

        insert_sql = f'''
                      INSERT INTO {table_name} ({columns})
                      VALUES ({placeholders})
                      '''

        self.cursor.execute(insert_sql, values)
        self.conn.commit()

    def remove_row(self, table_name: str, ID: int):
        condition = "id = ?"
        self.cursor.execute(f"DELETE from {table_name} WHERE {condition}", (ID,))
        self.conn.commit()

    def show_table(self, table_name: str):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def close_connection(self):
        self.conn.close()


# sql = SQLmanager('../../../zahav.db')
# sql.remove_row('calc_results', 5)

