import pymysql
import pandas as pd 
#import cryptography


class mysqlDB:  

    def __init__(self):
        # Database connection parameters
        self.host = '54.153.69.166'  # Replace with the IP address of the remote server
        self.user = 'client'    # Replace with your MySQL username
        self.password = 'dsci551' # Replace with your MySQL password
        self.database = 'CHATDB_39' # Replace with the name of your database
        self.port = 3306        
        self.connection = None
        self.imported_data = None 
        

    def connect(self): 
        try:
            # Establish a connection to the database
            self.connection = pymysql.connect(host= self.host,
                                        user= self.user,
                                        password= self.password,
                                        port= self.port, 
                                        database= self.database)
            if self.connection.open: 
                print("Connection successful")
            else: 
                print("Connection failed")

        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")

    def disconnect(self): 
            # Close the connection
            if 'connection' in locals():
                self.connection.close()

    def execute(self, query):
        with self.connection.cursor() as cursor: 
            cursor.execute(query)
        # Fetch all the results
        results = cursor.fetchall() 

        for row in results: 
            print(row) 
        return results 

    def top_n_rows(self, n, table_name):
        query = f"select * from {table_name} LIMIT {n}" 
        return self.execute(query) 


    def create_table(self, new_table_schema):
        self.execute(new_table_schema)
        return self.execute("show tables;")
    
    def drop_table(self, drop_table_schema):
        self.execute(drop_table_schema)
        return self.execute("show tables;")    

    def alter_table_schema(self, alter_table_schema): 
        self.execute(alter_table_schema) #alter table {table_name} modify {alter_table_schema}
        table_name = alter_table_schema.split(" ")[2]
        return self.execute(f"describe {table_name} ;")

    def insert_into(self,table_name): 
        # line-by-line approach 
        for row in self.imported_data.itertuples(index=False):
            insert_sql = f"INSERT INTO {table_name} VALUES"
            values = [f"'{i}'" if type(i) is str else str(i) for i in row]  
            row_str = ','.join(values) 
            insert_sql += f"({row_str})" 
            #print(insert_sql)
            
            self.execute(insert_sql)
            self.connection.commit() 
        print("Insert Done-!") 
    
    def bring_data(self, filepath):
        self.imported_data = None 
        if 'csv' in filepath:
            self.imported_data = pd.read_csv(filepath) 
        elif 'xlsx' in filepath: 
            self.imported_data = pd.read_excel(filepath)     

    def describe_table(self, table_name): 
        return self.execute(f"describe {table_name}")

    def show_grants(self): 
        grant_query = f"SHOW GRANTS FOR '{self.user}'@'%';"
        return self.execute(grant_query)
    
    def show_columns(self, table_name:str): 
        return self.execute(f"show columns from {table_name};") 
        

def main():
    test = mysqlDB() 
    test.disconnect() 
    test.connect()
    test.execute("select * from FRED;")
    
if __name__ == "__main__":
    main() 