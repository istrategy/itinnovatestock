import pandas as pd
import csv
import mysql.connector
import time
import datetime
from datetime import date
import yfinance as yf
import numpy as np
import pandas as pd
import json



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

    def setLabel(self, lastValue,lastPlus1):
        target = ((lastPlus1/lastValue)-1) *100
        retValue ="No change"
        if target < -5:
            retValue = 'down 5%'
        if target < -2 and target > -5:
            retValue = 'down 2-5%'
        if target < 0 and target > -2:
            retValue = ' down 0-2%'
        if target > 0 and target < 2:
            retValue = 'up 0-2%'
        if target > 2 and target < 5:
            retValue = 'up 2-5%'
        if target > 5:
            retValue = 'up 5%'
        return retValue, target


    def generateBlocks(self, shareArray, fromDate, toDate, blocksize):
        rowcounter =1
        arayCounter = 0
        resArray = []
        exitFunc = False
        batchArray = []
        targetArray =[]
        mydb = self.myconn()
        while exitFunc == False:
            block = []
            shareCounter = 0
            for item in shareArray:
                targetDateStart = fromDate
                row = []
                itemSql = "select price.tdate, company.name, company.symbol, price.close from company \
                                            left outer join price on company.id = price.company_id \
                                            WHERE company.symbol LIKE '" + item + "' and tdate >= '" + fromDate + "'  and tdate <= '" + toDate + "'\
                                            order by company.name,price.tdate limit 0,"+str(blocksize)
                # print(itemSql)
                mycursor = mydb.cursor()
                rowCounter = mycursor.execute(itemSql)
                myresult = mycursor.fetchall()

                if len(myresult) < blocksize:
                    exitFunc = True
                    break
                for x in myresult:
                    row.append(x[3])
                    lastDate = x[0]
                    lastValue= x[3]
                block.append(row)
                # print(row)
                # set target Array
                if shareCounter == 0 and exitFunc == False:
                    itemSql = "select price.tdate, company.name, company.symbol, price.close from company \
                                                                left outer join price on company.id = price.company_id \
                                                                WHERE company.symbol LIKE '" + item + "' and tdate > '" + str(lastDate) + "' LIMIT 1 "
                    # print(itemSql)
                    mycursor.execute(itemSql)
                    myresult = mycursor.fetchall()
                    for target in myresult:
                        targetArray.append([str(fromDate), self.setLabel(lastValue,target[3]),target[2],lastValue, target[3]])
                        # print(targetArray)
                shareCounter += 1

            if exitFunc == False:
                batchArray.append(block)
            fromDate = str(lastDate)


        batchNp = np.array(batchArray)
        print(batchArray)

        # targetNp = np.array(targetArray)
        # print(print(targetNp))

        # pd.DataFrame(batchNp).to_csv("batch.csv")
        # print(batchArray)
        # print(targetArray)
        # print(lastDate)

        mycursor.close()
        mydb.close()

        return json.dumps(targetArray)




updaeObj = updateData()

startDate = "2010-01-01"
startDate = "2021-12-01"
# endDate = date.today()
endDate = '2022-01-01'
# print(startDate, endDate)
shareArray=['SLM.JO','ABG.JO','SOL.JO','TKG.JO']

blocksize = 10

print(updaeObj.generateBlocks(shareArray, startDate, endDate, blocksize))
