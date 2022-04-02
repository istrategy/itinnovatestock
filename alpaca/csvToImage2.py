import numpy as np
from PIL import Image
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

class csvToImage:
    def generatePixelArrayFile(self):
        print('GENERATE FILE')
        a = np.array(self.generatePixelArray())
        print(a)
        np.savetxt('colors.csv', a, delimiter=',')
        print('File generated.')


    def generatePixelArray(self):
        print('Generate Pixel Array')
        returnArray  = []
        counter = 0
        for r in range (0,256):
            # print(r)
            for g in range(0, 256):
                for b in range(0, 256):
                    # print(str(r),str(g), str(b))
                    returnArray.append([counter,(r,g,b)])
                    counter += 1
                    if counter > 1000000:
                        break
        return returnArray



    def convertImage(self, inputCsvFile, targetFolder, bigFiles):

        pixelArray = self.generaelAtePixrray();
        print('ConvertImage')
        blocksize = 50
        base_name = inputCsvFile.split('\\')[-1]
        saving_name = base_name[0:-4] + ".png"
        print('csvToImage')
        with open(inputCsvFile) as file:
            array = np.loadtxt(file, delimiter=',', skiprows=1)
            print(array.shape)
            rows = array.shape[0] * blocksize
            cols = array.shape[1] * blocksize
            # print(rows)
            img = Image.new('RGB', (array.shape[1], array.shape[0]))
            rowcounter = 0
            for row in array:
                colcounter = 0
                print(row)
                for col in row:
                    print("LOOP:",colcounter, rowcounter)

                    arraypos = int(col *10)
                    img.putpixel((colcounter, rowcounter), (pixelArray[int(arraypos)][1][0], pixelArray[int(arraypos)][1][1], pixelArray[int(arraypos)][1][2], 255))
                    print(pixelArray[int(arraypos)])
                    colcounter += 1

                rowcounter += 1
            #
            # img.putpixel((3, 3), (200, 200, 100, 255))
            # img.putpixel((8, 3), (200, 200, 0, 255))
            # img.putpixel((9, 3), (200, 200, 200, 255))
            img.save(os.path.join(targetFolder , saving_name))
            if bigFiles == True:
                resized_img = img.resize((cols,rows),resample=0,)
                resized_img.save(os.path.join("./data/big/" , saving_name))


    def convertImageGraph(self, inputCsvFile, targetFolder, bigFiles):

        # pixelArray = self.generatePixelArray();
        print('ConvertImage')
        blocksize = 50
        base_name = inputCsvFile.split('\\')[-1]
        saving_name = base_name[0:-4] + ".png"
        print('csvToImage')
        with open(inputCsvFile) as file:
            array = np.loadtxt(file, delimiter=',', skiprows=1)
            print(array.shape)
            rows = array.shape[0] * blocksize
            cols = array.shape[1] * blocksize
            # print(rows)
            # img = Image.new('RGB', (array.shape[1], array.shape[0]))
            rowcounter = 0
            numberRows = 2
            # if rowcounter >= numberRows:
            #     break
            colcounter = 0
            # print(row)
            print(len(array[0]))

            arrayCounter = 0
            Data = {}
            stopCounter = 2
            for item in range(0, len(array)):
                if arrayCounter == 0:
                    header = list(range(1, len(array[0]) + 1))
                    Data['header'] = header
                Data['row'+str(arrayCounter)] = array[arrayCounter]
                arrayCounter += 1
                if arrayCounter >= stopCounter:
                    break
            df = pd.DataFrame(Data)

            fig, ax1 = plt.subplots()
            color = 'tab:red'
            ax1.plot(header, df['row0'], color=color)
            color = 'tab:blue'
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            # ax2.set_ylabel('Volume', color=color)
            ax2.set_ylim(0, 50000000)
            # ax2.plot()
            ax2.plot(header, df['row1'], color=color)


            # for key, value in df.items():
            #     if key != 'header':
            #         color = 'tab:red'
            #         ax1.plot(header, value, color=color)
            #         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            #         ax2.plot(header, value, color=color)
            #     print(key, '->', value)





            # color = 'tab:blue'
            # # ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
            # ax2.plot(header, df['Vol'], color=color)
            # ax2.tick_params(axis='y', labelcolor=color)


            plt.grid(True)
            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            # plt.show()
            plt.savefig(os.path.join(targetFolder, saving_name))
            plt.close()

            # for row in array:

    def convertImages(self, sourceFolder,targetFolder,bigFiles):
        for subdir, dirs, files in os.walk(sourceFolder):
            # print(dirs)
            for dir in dirs:
                # loopdir = os.path.join(sourceFolder,dir)
                print(dir)
                for subdir1, dirs1, files1 in  os.walk(os.path.join(sourceFolder,dir)):
                    print(files1)
                    for file in files1:
                        print(file)
                        fullfilepath = os.path.join(sourceFolder,dir,file)
                        print(fullfilepath)
                        targetpath = os.path.join(targetFolder,dir)
                        if not os.path.exists(targetpath):
                            os.makedirs(targetpath)
                        print(targetpath)
                        self.convertImageGraph(fullfilepath,targetpath,bigFiles)





            # for sdir in dirs:
            #     print(sdir)

            # for file in files:
            #     print(file)
                # os.path.join(subdir, file)
# cObj = csvToImage()
# csvFile = "./data/SLM.JO/2015-08-07.csv"
targetFolder = "./data/SLM.JO/"


sourceFolder = "./data/csv/SLM.JO/"

cObj = csvToImage()

# cObj.convertImage(csvFile,targetFolder)

# F:\itinnovatedata\20220401_224126\images
sourceFolder = "F://itinnovatedata//20220401_224126//csv"
targetFolder = "F://itinnovatedata//20220401_224126//images"
bigFiles = True
cObj.convertImages(sourceFolder,targetFolder,bigFiles)





