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
import matplotlib.pyplot as plt

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

    def setLabelTrend(self, rowTarget):
        x = range(0, len(rowTarget))
        resultTrend = np.polyfit(x, rowTarget, 1)
        retString = 'sidew'
        if resultTrend[0] <= -5:
            retString = 'down5'
        if resultTrend[0] >= 5:
            retString = 'up5'

        return [retString, resultTrend]

    def setLabelTrendBinary(self, lastValue, targetValue):
        if lastValue < targetValue:
            retString = str('1')
        else:
            retString = str('0')

        return retString

    def saveCSVname(self, basepath, targetsubfolder, dataFrame,fullDF):

        folder = os.path.join(basepath['csv'],targetsubfolder)

        if not os.path.exists(folder):
            os.makedirs(folder)
        folderimages = os.path.join(basepath['images'], targetsubfolder)

        if not os.path.exists(folderimages):
            os.makedirs(folderimages)

        # print(dataFrame)
        tDate =str(dataFrame['tdate'].values[-1])
        companyCode = dataFrame['symbol'].values[-1]
        # print((tDate))
        # print(str(companyCode))


        tfilename = companyCode +"_"+tDate + '.csv'
        imageFilename = companyCode +"_"+tDate + '.png'
        # print(folder)
        print(tfilename)
        SavePath = os.path.join(folder,tfilename)
        dataFrame.to_csv(SavePath)

        # take out last 5 records the aim is to predict it
        dataFrame = dataFrame[:-1]

        x = range(dataFrame.shape[0])
        y = dataFrame["close"].values.tolist()
        y2 = dataFrame["volume"].values.tolist()
        # fig, ax = plt.subplots()
        # ax.plot(x,y)
        # ax.plot(x, y2)
        # plt.show()

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('price', color=color)
        ax1.plot(x,y, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('volume', color=color)  # we already handled the x-label with ax1
        ax2.plot(x, y2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.savefig(os.path.join(folderimages, imageFilename))

        plt.close()




    def generateBlocks(self, shareArray, fromDate, toDate, blocksize,paths,labelPerc=0.25):
        rowcounter =1
        arayCounter = 0
        resArray = []
        exitFunc = False
        batchArray = []
        targetArray =[]
        mydb = self.myconn()
        datablocknum = int(blocksize- (blocksize*labelPerc))
        labelblocknum = blocksize - datablocknum

        while exitFunc == False:
            block = []
            shareCounter = 0
            for item in shareArray:
                targetDateStart = fromDate
                row = []
                rowvol = []
                header = []
                rowTarget = []
                itemSql = "select price.tdate, company.name, company.symbol, price.close, price.volume from company \
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

                    if colcounter < datablocknum:
                        header.append('col' + str(colcounter))
                        row.append(x[3])
                        rowvol.append(x[4])
                    elif colcounter < datablocknum:
                        header.append('col' + str(colcounter))
                        row.append(x[3])
                        rowvol.append(x[4])
                        if shareCounter == 0:
                            rowTarget.append(x[3])
                    else:
                        if shareCounter == 0:
                            rowTarget.append(x[3])
                    lastDate = x[0]
                    lastValue= x[3]
                    colcounter += 1
                if shareCounter == 0:
                    block.append(header)
                    # block.append(rowTarget)
                block.append(row)
                block.append(rowvol)
                # print(row)
                # set target Array
                if shareCounter == 0 and exitFunc == False: # get next date and set filename
                    # print('TEST')
                    itemSql = "select price.tdate, company.name, company.symbol, price.close from company \
                                                                left outer join price on company.id = price.company_id \
                                                                WHERE company.symbol LIKE '" + item + "' and tdate > '" + str(lastDate) + "' LIMIT 1 "
                    # # print(itemSql)
                    mycursor.execute(itemSql)
                    myresult = mycursor.fetchall()
                    for target in myresult:
                        targetString = [str(fromDate), self.setLabelTrend(rowTarget)]
                        targetArray.append([str(fromDate), targetString])
                        newStartDate = str(target[0])



                shareCounter += 1

            if exitFunc == False:
                batchArray.append(block)
                self.saveCSV(fromDate, targetString, block,paths['csv'],rowTarget)
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

    def generateOneCompany(self, shareCode, fromDate, toDate, blocksize,paths,labelPerc):
        print(shareCode)
        itemSql = "select price.tdate, company.name, company.symbol, price.close, price.volume from company \
                                            left outer join price on company.id = price.company_id \
                                            WHERE company.symbol = '" + shareCode + "' and tdate >= '" + fromDate + "'  and tdate <= '" + toDate + "'\
                                            order by company.name,price.tdate "
        mydb = self.myconn()
        mycursor = mydb.cursor()
        df = pd.read_sql(itemSql, mydb)
        fullDF = df
        activeBlocks = df.shape[0]
        while activeBlocks >= blocksize:
            subframe = df[:blocksize]
            # target = self.setLabelTrend(subframe[:])
            # df.iloc[:, :-int(blocksize/labelPerc)]
            # print(subframe)

            predValue = subframe[blocksize-1:]['close'].values[0]

            lastValue = subframe[blocksize-2:-1]['close'].values[0]

            # print(lastpart['close'])
            target = self.setLabelTrendBinary(lastValue, predValue)
            self.saveCSVname(paths,target[0],subframe,fullDF)


            df = df[blocksize:]
            # print(df.shape[0])
            activeBlocks = df.shape[0]

            # df.to_csv('out.csv')

        # for blockCounter in range(blocksize):
        #     print(blockCounter)

    def generateBlocksExpanded(self, shareArray, fromDate, toDate, blocksize,paths,labelPerc=0.25):
        for shareCode in shareArray:
            self.generateOneCompany(shareCode, fromDate, toDate, blocksize,paths,labelPerc)


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
        tdate = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        returnDict = {}
        for item in types:
            fullpath = os.path.join(basepath,tdate,item)
            os.makedirs(fullpath)
            returnDict[item] = fullpath
        # createSavepath
        print(fullpath)
        return returnDict

    def getShares(self):
        counter = 1
        returnArray = []
        # itemSql = "select  * FROM company LIMIT 0 ,20"
        itemSql = "select  * FROM company"
        mydb = self.myconn()
        mycursor = mydb.cursor()
        df = pd.read_sql(itemSql, mydb)

        mycursor = mydb.cursor()
        rowCounter = mycursor.execute(itemSql)
        myresult = mycursor.fetchall()

        for x in myresult:
            print(x[1], counter)
            counter += 1
            returnArray.append(x[1])
        return returnArray






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
# print(paths)
labelPerc = 0.95
shareArray = updaeObj.getShares()
paths = updaeObj.createSavepath(basepath,['csv','images'])
#
updaeObj.generateBlocksExpanded(shareArray, startDate, endDate, blocksize,paths, labelPerc)

#note
# Generate 20 days files
# predict 1 / 0