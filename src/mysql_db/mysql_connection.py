import configparser
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

# Read database configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

class MySQLConnectionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnectionSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.host = config['mysqlDB']['host']
        self.user_name = config['mysqlDB']['user']
        self.password = config['mysqlDB']['pass']
        self.database = config['mysqlDB']['db']
        self._connection = None
        self._cursor = None
        self._engine = None
        self._initialized = True

    def connectDB_get_cursor(self):
        if not self._connection:
            try:
                # Connect to MySQL server
                self._connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user_name,
                    password=self.password
                )
                if self._connection.is_connected():
                    print("Connected to MySQL server")
                    self._cursor = self._connection.cursor(buffered=True)
                    
                    # Create database if it does not exist
                    self._cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                    
                    # Use the created database
                    self._cursor.execute(f"USE {self.database}")
                else:
                    print("Failed to connect to MySQL server")
                    self._connection = None
                    self._cursor = None
            except Error as e:
                print(f"Error: {e}")
                self._connection = None
                self._cursor = None
        return self._cursor

    def get_mysql_engine(self):
        if not self._engine:
            try:
                self._engine = create_engine(f"mysql+mysqlconnector://{self.user_name}:{self.password}@{self.host}/{self.database}")
                print("SQLAlchemy engine created")
            except Error as e:
                print(f"Error creating SQLAlchemy engine: {e}")
                self._engine = None
        return self._engine

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

# Create a single instance to be used across the application
mysql_singleton = MySQLConnectionSingleton()
