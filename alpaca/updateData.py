import pandas as pd
import csv
import mysql.connector
import time
import datetime
from datetime import date
import yfinance as yf


class updateData:
    # filename = './data/JSE202202151d.csv'

    def myconn(self):
        myconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="stock"
        )
        return myconn


    def loadAll(self, startDate,endDate):
        sqlSelect = "SELECT * from company "
        # print(sqlSelect)
        mydb = self.myconn()
        mycursor = mydb.cursor()
        rowCounter = mycursor.execute(sqlSelect)
        myresult = mycursor.fetchall()
        counter = 0
        for x in myresult:
            print(x)
            data = yf.download(x[1], start=startDate, end=endDate)
            # print((data))

            for index, row in data.iterrows():
                mydb = self.myconn()
                mycursor = mydb.cursor()
                # print(index,row[0])
                # print(row[0])
                # print(index)
                # print(str(index)[:10])

                sql = "INSERT INTO price (company_id,tdate ,open ,high , low,close ,adjclose ,volume) VALUES ( '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}'  )".format(
                    x[0], str(index)[:10], row[0], row[1], row[2], row[3], row[4], row[5])
                # print(sql)
                try:
                    mycursor.execute(sql)
                    mydb.commit()
                except:
                    print("Error move to the next line")


                mycursor.close()
                mydb.close()
            print(x)
            time.sleep(10)




updaeObj = updateData()

startDate = "2003-01-01"
# endDate = date.today()
endDate = '2004-01-01'
print(startDate, endDate)

updaeObj.loadAll(startDate,endDate)

# endDate = '2022-01-31'
# updaeObj.loadAll(startDate,endDate)
