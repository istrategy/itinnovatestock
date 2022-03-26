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
from functions.IGTD_Functions import min_max_transform, table_to_image


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
        retValue ="equal"
        if target < -5:
            retValue = 'down5'
        if target < -2 and target > -5:
            retValue = 'down2_5'
        if target < 0 and target > -2:
            retValue = 'down0_2'
        if target > 0 and target < 2:
            retValue = 'up0_2'
        if target > 2 and target < 5:
            retValue = 'up2_5'
        if target > 5:
            retValue = 'up5'
        return retValue, target

    def saveCSV(self, target, targetString, block, savefolder):
        folder = savefolder
        # folder = "./data/csv/"+target[2]
        if not os.path.exists(folder):
            os.makedirs(folder)
        # targetfolder
        folder = folder + "/" + targetString[1][0]
        if not os.path.exists(folder):
            os.makedirs(folder)

        targetDate = target[0].strftime("%Y-%m-%d")
        # tfilename = targetString[0]  + "__" + targetDate +"__" + str(target[3]) +"_LABEL_"+targetString[1][0]+ '.csv'
        tfilename = targetDate + '.csv'

        filename = folder + "/" + tfilename
        # print(filename)
        with open(filename, 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            for item in block:
                # print(item)
                writer.writerow(item)

    def generateBlocks(self, shareArray, fromDate, toDate, blocksize,paths,labelPerc=0.25):
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
                header = []
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
                colcounter = 1
                for x in myresult:
                    if colcounter == 2:
                        secondDate = x[0]
                    header.append('col'+str(colcounter))
                    row.append(x[3])
                    lastDate = x[0]
                    lastValue= x[3]
                    colcounter += 1
                if shareCounter == 0:
                    block.append(header)
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
                self.saveCSV(target, targetString, block,paths['csv'])
            # fromDate = str(lastDate)
            fromDate = str(newStartDate)
            fromDate = str(secondDate)



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

    def test(self):
        num_row = 2  # Number of pixel rows in image representation
        num_col = 10  # Number of pixel columns in image representation
        num = num_row * num_col  # Number of features to be included for analysis, which is also the total number of pixels in image representation
        save_image_size = 3  # Size of pictures (in inches) saved during the execution of IGTD algorithm.
        max_step = 10000  # The maximum number of iterations to run the IGTD algorithm, if it does not converge.
        val_step = 300  # The number of iterations for determining algorithm convergence. If the error reduction rate
        # is smaller than a pre-set threshold for val_step itertions, the algorithm converges.

        # data = pd.read_csv('./Data/Data.txt', low_memory=False, sep='\t', engine='c', na_values=['na', '-', ''],
        #                    header=0, index_col=0)
        data = pd.read_csv('./Data/SLM.JO/2010-01-01__2010-01-15__2262.0_LABEL_down_0-2perc.csv', low_memory=False, sep=',', engine='c', na_values=['na', '-', ''],
                           header=0, index_col=0)
        print(data.shape)
        data = data.iloc[:, :num]
        norm_data = min_max_transform(data.values)
        norm_data = pd.DataFrame(norm_data, columns=data.columns, index=data.index)
        # print(data.index)
        # print(data.info())
        # print(data.shape)
        # print(data.count())
        fea_dist_method = 'Euclidean'
        image_dist_method = 'Euclidean'
        error = 'abs'
        result_dir = '../Results/Test_1'
        os.makedirs(name=result_dir, exist_ok=True)
        table_to_image(norm_data, [num_row, num_col], fea_dist_method, image_dist_method, save_image_size,
                       max_step, val_step, result_dir, error)
        print("ConvertImage")

    def createSavepath(self, basepath, types):
        print('createSavepath')
        tdate = datetime.datetime.today().strftime('%Y%m%d_%H%M')
        returnDict = {}
        for item in types:
            fullpath = os.path.join(basepath,tdate,item)
            os.makedirs(fullpath)
            returnDict[item] = fullpath
        # createSavepath
        print(fullpath)
        return returnDict


updaeObj = updateData()

startDate = "2010-01-01"
# startDate = "2021-11-01"
# endDate = date.today()
endDate = '2022-01-01'
# print(startDate, endDate)
shareArray=['SLM.JO',
            'ABG.JO',
            'SOL.JO'
            ,'AGL.JO'
            ,'BAT.JO'
            ,'DRD.JO'
            ,'FSR.JO'
            ,'MTN.JO'
            ,'PSG.JO'
            ,'SUR.JO'
]

blocksize = 20

basepath = "F:\itinnovatedata"
# savecsvfolder =
paths = updaeObj.createSavepath(basepath,['csv','images'])
# print(paths)
labelPerc = 0.25

updaeObj.generateBlocks(shareArray, startDate, endDate, blocksize,paths, labelPerc)
