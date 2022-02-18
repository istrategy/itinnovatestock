import pandas as pd
import csv
import mysql.connector
import time
import datetime
import yfinance as yf

class importData:
    filename = './data/JSE202202151d.csv'

    def myconn(self):
        myconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="stock"
        )
        return myconn

    def importData(self):
        fields = []
        rows = []

        # reading csv file
        with open(self.filename, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields = next(csvreader)

            # extracting each data row one by one
            for row in csvreader:
                mydb = self.myconn()
                mycursor = mydb.cursor()
                print(row)
# //                sql = "INSERT INTO company  (VALUES (%s, %s, %s, %s, %s, %s)"

                if row[5] == 'N/A':
                    val5 = '0'
                else:
                    val5 = row[5]
                val = (row[0], row[1], row[2], row[3], row[4], val5)
                sql = "INSERT INTO company (id, symbol, name, price, changeval, changeprc, peratio) VALUES (null, '{}',  '{}',  '{}',  '{}',  '{}',  '{}'  )".format(row[0], row[1], row[2], row[3], row[4], val5)
                print(sql)
                try:
                    mycursor.execute(sql)
                    mydb.commit()
                except:
                    print("Error move to the next line")


                mycursor.close()
                mydb.close()



id = importData()

id.importData()
