import pyodbc
import pandas as pd

class DTB_dataset:
    def __init__(self):
        #-----------------------Setup DTB-----------------------
        self.DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
        self.SERVER_NAME = 'HOLAKAKA-PC'  # SELECT @@SERVERNAME
        self.DATABASE_NAME = 'datasource'
        self.DATABASE_UID = 'nckh'
        self.DATABASE_PWD = '123456'

        self.connection_string = f"""
        DRIVER={{{self.DRIVER_NAME}}};
        SERVER={self.SERVER_NAME};
        DATABASE={self.DATABASE_NAME};
        UID={self.DATABASE_UID};
        PWD={self.DATABASE_PWD};
        Trus_Connection = yes;
        """
        #-----------------------Connect DTB-----------------------
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    def query_table(self,sql):
        """
        Truy vấn Database
        - Input: String
        - Output: List
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def create_table(self,table_name,list_col):
        """
        - Input: String: table_name, List: list_col
        - Output: boolean
        """
        try:
            create_value = 'CREATE TABLE ' + table_name + ' ('
            first = True
            for col in list_col:
                if first:
                    first = False
                else:
                    create_value += ', '

                type_col = col + ' varchar(1000)'
                create_value += type_col
                
            
            create_value += ')' 
            self.cursor.execute(create_value)
            self.conn.commit()   
            return True
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print(sqlstate)
            return sqlstate

    def update_table(self,table_name,data):
        """
        - Input: String: table_name, Dataframe: data
        - Output: boolean
        """
        try:
            # Set a counter, since there can't be more than 1000 inserts at a time
            counter = 0
            # Create the header row
            values_index = 'VALUES ('
            header_row = 'INSERT INTO ' + table_name + ' ('
            first = True
            for col in data.columns:
                if first:
                    first = False
                else:
                    header_row += ', '
                    values_index += ','
                header_row += col
                values_index += '?'
            
            header_row += ') ' + values_index + ')'

            # Insert DataFrame to Table
            for row in data.itertuples(index=False, name=None): 
                self.cursor.execute(header_row,tuple(row))
                if counter % 1000 == 0:
                    self.conn.commit()
                # Increase counter
                counter += 1     
            self.conn.commit()
            return True
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print(sqlstate)
            return False


# ------------------------Example------------------------
# maindata = DTB_dataset()
# sql="select * from example"
# data=maindata.query_table(sql)
# print(data)
# df = pd.DataFrame(data)
# print(df)

# table_name = "exp_create"
# col_name = ["mot","hai","ba"]
# bool_create = maindata.create_table(table_name,col_name)
# print(bool_create)
