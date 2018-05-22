import sqlite3


class DatabaseException(Exception):
    pass


class Database:

    def __init__(self, database_name, backend='sqlite'):
        """ Now Database class only accepts 'sqlite' backend. However it's build in this way to allow more backends in
        the future."""
        self.database_name = database_name
        self.backend = backend
        self.connexion = sqlite3.connect(database_name)
        self.cursor = self.connexion .cursor()

    def _raise_not_implemented(self):
        raise NotImplementedError('Method not implemented for "{}" backend.'.format(self.backend))

    def get_database_name(self):
        """ Returns database_name"""
        return self.database_name

    def get_table_names(self):
        """ Return a list of the names of all the tables"""
        if self.backend == 'sqlite':
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result = self.cursor.fetchall()
            return [table for sublist in result for table in sublist]
        else:
            self._raise_not_implemented()

    def create_table(self, table_name, columns):
        """ Creates a table.

            table_name: string-name
            columns: dictionary with
        """
        try:
            if self.backend == 'sqlite':
                column_list = ['{} {}'.format(key, value) for key, value in columns.items()]
                initial = 'CREATE TABLE {} ({})'.format(table_name, ', '.join(column_list))
                self.cursor.execute(initial)
                self.connexion.commit()
            else:
                self._raise_not_implemented()
        except Exception as e:
            raise DatabaseException('There was an error trying to create the table "{}": "{}"'.format(table_name, e))

    def insert_into(self, table_name, values):
        """
        Insert values into a table.

            table_name: string-name
            values: dictionary. Example: {'key': keyword, 'value': value}
        """
        self.cursor.execute('INSERT INTO {} ({}) VALUES({})'.format(table_name, ', '.join(values.keys()),
                                                                    '"{}"'.format('", "'.join(values.values()))))
        self.connexion.commit()

    # TODO: Implement next methods:
    # def retrieve_from(self, table_name, )
    # delete_database()
