import sqlite3


class DatabaseConnection:
    """
    Context manager created to connect with the SQLint database
    """
    def __init__(self, host) -> None:
        """
        It is the constructor of the class that is also used to define the variables of the class
        that can be used by the other methods.
        """
        self.connection = None
        self.host = host

    def __enter__(self) -> sqlite3.Connection:
        """
        Function that will start the connection and will create the cursor for the development
        :return: the cursor
        """
        self.connection = sqlite3.connect(self.host)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Method that will finalize the connection. If some error occurs, it will close the connection
        """
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
