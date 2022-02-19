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
import os
import csv

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
        retValue ="no_change"
        if target < -5:
            retValue = 'down_5perc'
        if target < -2 and target > -5:
            retValue = 'down_2-5perc'
        if target < 0 and target > -2:
            retValue = 'down_0-2perc'
        if target > 0 and target < 2:
            retValue = 'up_0-2perc'
        if target > 2 and target < 5:
            retValue = 'up_2-5perc'
        if target > 5:
            retValue = 'up_5perc'
        return retValue, target

    def saveCSV(self, target,targetString,block):
        folder = "./data/"+target[2]
        if not os.path.exists(folder):
            os.makedirs(folder)

        targetDate = target[0].strftime("%Y-%m-%d")
        tfilename = targetString[0]  + "__" + targetDate +"__" + str(target[3]) +"_LABEL_"+targetString[1][0]+ '.csv'
        filename =  folder + tfilename
        # print(filename)
        with open(filename, 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            for item in block:
                # print(item)
                writer.writerow(item)

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
                        targetString = [str(fromDate), self.setLabel(lastValue,target[3]),target[2],lastValue, target[3]]
                        targetArray.append([str(fromDate), self.setLabel(lastValue,target[3]),target[2],lastValue, target[3]])
                        newStartDate = str(target[0])
                        # self.saveCSV(target,targetString,row)
                        # print(targetArray)

                shareCounter += 1

            if exitFunc == False:
                batchArray.append(block)
                self.saveCSV(target, targetString, block)
            # fromDate = str(lastDate)
            fromDate = str(newStartDate)


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
# startDate = "2021-11-01"
# endDate = date.today()
endDate = '2022-01-01'
# print(startDate, endDate)
shareArray=['SLM.JO','ABG.JO','SOL.JO','TKG.JO']

blocksize = 10

updaeObj.generateBlocks(shareArray, startDate, endDate, blocksize)
